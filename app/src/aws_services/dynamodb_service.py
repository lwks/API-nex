from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import boto3
from boto3.session import Session


class DynamoDBService:
    """High-level DynamoDB helper focused on CRUD operations."""

    def __init__(
        self,
        table_name: str,
        *,
        region_name: Optional[str] = None,
        session: Optional[Session] = None,
        endpoint_url: Optional[str] = None,
    ) -> None:
        """
        Create a DynamoDB service wrapper.

        Args:
            table_name: Target DynamoDB table name.
            region_name: AWS region. Ignored if a Session is provided.
            session: Existing boto3 session to reuse.
            endpoint_url: Custom endpoint (useful for localstack or tests).
        """
        self._table_name = table_name
        self._resource = (
            session.resource("dynamodb", endpoint_url=endpoint_url)
            if session
            else boto3.resource(
                "dynamodb", region_name=region_name, endpoint_url=endpoint_url
            )
        )
        self._table = self._resource.Table(table_name)

    async def get(
        self,
        key: Dict[str, Any],
        *,
        consistent_read: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a single item by key."""
        response = await asyncio.to_thread(
            self._table.get_item,
            Key=key,
            ConsistentRead=consistent_read,
        )
        return response.get("Item")

    async def create(
        self,
        item: Dict[str, Any],
        *,
        condition_expression: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Insert a new item. Optionally enforces a condition expression."""
        kwargs: Dict[str, Any] = {"Item": item}
        if condition_expression is not None:
            kwargs["ConditionExpression"] = condition_expression

        await asyncio.to_thread(self._table.put_item, **kwargs)
        return item

    async def update(
        self,
        key: Dict[str, Any],
        attributes: Dict[str, Any],
        *,
        condition_expression: Optional[str] = None,
        return_values: str = "ALL_NEW",
    ) -> Dict[str, Any]:
        """
        Update one or more attributes for the provided key.

        Args:
            key: The primary key (and sort key if applicable).
            attributes: Attribute names and their new values.
            condition_expression: Optional condition expression.
            return_values: DynamoDB ReturnValues flag (default ALL_NEW).
        """
        if not attributes:
            raise ValueError("attributes cannot be empty for an update operation.")

        update_fragments: list[str] = []
        expr_attr_names: Dict[str, str] = {}
        expr_attr_values: Dict[str, Any] = {}

        for idx, (attr, value) in enumerate(attributes.items()):
            name_placeholder = f"#attr{idx}"
            value_placeholder = f":val{idx}"
            expr_attr_names[name_placeholder] = attr
            expr_attr_values[value_placeholder] = value
            update_fragments.append(f"{name_placeholder} = {value_placeholder}")

        update_expression = "SET " + ", ".join(update_fragments)

        kwargs: Dict[str, Any] = {
            "Key": key,
            "UpdateExpression": update_expression,
            "ExpressionAttributeNames": expr_attr_names,
            "ExpressionAttributeValues": expr_attr_values,
            "ReturnValues": return_values,
        }
        if condition_expression is not None:
            kwargs["ConditionExpression"] = condition_expression

        response = await asyncio.to_thread(self._table.update_item, **kwargs)
        return response.get("Attributes", {})

    async def list(
        self,
        *,
        limit: Optional[int] = None,
        consistent_read: bool = False,
    ) -> list[Dict[str, Any]]:
        """
        List items using Scan. Suitable for admin screens or small datasets.
        """
        scan_kwargs: Dict[str, Any] = {"ConsistentRead": consistent_read}
        if limit is not None:
            scan_kwargs["Limit"] = limit

        items: list[Dict[str, Any]] = []
        last_evaluated_key: Optional[Dict[str, Any]] = None

        while True:
            if last_evaluated_key is not None:
                scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

            response = await asyncio.to_thread(self._table.scan, **scan_kwargs)
            items.extend(response.get("Items", []))
            last_evaluated_key = response.get("LastEvaluatedKey")

            if last_evaluated_key is None:
                break
            if limit is not None and len(items) >= limit:
                break

        if limit is not None:
            return items[:limit]
        return items

    async def delete(self, key: Dict[str, Any]) -> bool:
        """Delete an item by key. Returns True if an item was removed."""
        response = await asyncio.to_thread(
            self._table.delete_item,
            Key=key,
            ReturnValues="ALL_OLD",
        )
        return "Attributes" in response
