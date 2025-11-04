"use client";

import { ChangeEvent, FormEvent, useMemo, useState } from "react";

type SelectOption = {
  label: string;
  value: string;
};

type JobFormState = {
  title: string;
  description: string;
  level?: string;
  position: string;
  publicationDate: string;
  hiringFormat: string;
};

const levelOptions: SelectOption[] = [
  { label: "Junior", value: "junior" },
  { label: "Pleno", value: "pleno" },
  { label: "Senior", value: "senior" },
  { label: "Especialista", value: "especialista" },
];

const positionOptions: SelectOption[] = [
  { label: "Estagiário", value: "estagiario" },
  { label: "Coordenador", value: "coordenador" },
  { label: "Analista", value: "analista" },
  { label: "Supervisor", value: "supervisor" },
  { label: "Gerente", value: "gerente" },
];

const hiringFormatOptions: SelectOption[] = [
  { label: "PJ", value: "pj" },
  { label: "Integral", value: "integral" },
  { label: "Temporário", value: "temporario" },
  { label: "Meio período", value: "meio-periodo" },
];

const defaultFormState: JobFormState = {
  title: "",
  description: "",
  level: undefined,
  position: "",
  publicationDate: "",
  hiringFormat: "",
};

export default function CreateJobPage() {
  const [form, setForm] = useState<JobFormState>(defaultFormState);

  const minPublicationDate = useMemo(() => {
    const today = new Date();
    const offset = today.getTimezoneOffset();
    const localDate = new Date(today.getTime() - offset * 60 * 1000);
    return localDate.toISOString().split("T")[0];
  }, []);

  const handleChange = (field: keyof JobFormState) =>
    (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      const value = event.target.value;
      setForm((prev) => ({
        ...prev,
        [field]: value,
      }));
    };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.table(form);
  };

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="mb-6 text-2xl font-semibold">Criar vaga</h1>
      <form className="space-y-6" onSubmit={handleSubmit}>
        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="title">
            Título
          </label>
          <input
            className="w-full rounded border border-slate-300 p-3"
            id="title"
            name="title"
            onChange={handleChange("title")}
            required
            type="text"
            value={form.title}
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="description">
            Descrição
          </label>
          <textarea
            className="w-full rounded border border-slate-300 p-3"
            id="description"
            name="description"
            onChange={handleChange("description")}
            required
            rows={5}
            value={form.description}
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="level">
            Nível (opcional)
          </label>
          <select
            className="w-full rounded border border-slate-300 p-3"
            id="level"
            name="level"
            onChange={handleChange("level")}
            value={form.level ?? ""}
          >
            <option value="">Selecione um nível</option>
            {levelOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="position">
            Cargo
          </label>
          <select
            className="w-full rounded border border-slate-300 p-3"
            id="position"
            name="position"
            onChange={handleChange("position")}
            required
            value={form.position}
          >
            <option value="">Selecione um cargo</option>
            {positionOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="publicationDate">
            Data de Publicação
          </label>
          <input
            className="w-full rounded border border-slate-300 p-3"
            id="publicationDate"
            min={minPublicationDate}
            name="publicationDate"
            onChange={handleChange("publicationDate")}
            required
            type="date"
            value={form.publicationDate}
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium" htmlFor="hiringFormat">
            Formato de Contratação
          </label>
          <select
            className="w-full rounded border border-slate-300 p-3"
            id="hiringFormat"
            name="hiringFormat"
            onChange={handleChange("hiringFormat")}
            required
            value={form.hiringFormat}
          >
            <option value="">Selecione um formato</option>
            {hiringFormatOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex justify-end gap-4">
          <button
            className="rounded border border-slate-300 px-6 py-3 text-sm font-medium"
            onClick={() => setForm(defaultFormState)}
            type="button"
          >
            Limpar
          </button>
          <button
            className="rounded bg-blue-600 px-6 py-3 text-sm font-semibold text-white"
            type="submit"
          >
            Salvar vaga
          </button>
        </div>
      </form>
    </main>
  );
}
