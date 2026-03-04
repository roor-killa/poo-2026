"use client";

import { useEffect, useState, useCallback } from "react";
import { fastapi, adminApi, type Mot, type MotDetail, type DefinitionWithId } from "@/lib/api";
import { useAuthStore } from "@/lib/auth";
import { Button }             from "@/components/ui/button";
import { Card, CardContent }  from "@/components/ui/card";

const CATEGORIES = [
  "", "nom", "vèb", "adjektif", "advèb", "pwonon",
  "prépoziksyon", "konjonksyon", "entèjèksyon", "atik", "lòt",
];

// ── Modal générique ────────────────────────────────────────────────────
function Modal({ title, onClose, children }: {
  title:    string;
  onClose:  () => void;
  children: React.ReactNode;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/50 p-4 pt-16">
      <div className="w-full max-w-lg rounded-xl bg-white shadow-xl dark:bg-zinc-900">
        <div className="flex items-center justify-between border-b px-5 py-3 dark:border-zinc-700">
          <h2 className="font-semibold text-zinc-900 dark:text-zinc-50">{title}</h2>
          <button onClick={onClose} className="text-zinc-400 hover:text-zinc-700">✕</button>
        </div>
        <div className="max-h-[70vh] overflow-y-auto p-5">{children}</div>
      </div>
    </div>
  );
}

// ── Formulaire d'édition d'une définition ─────────────────────────────
function DefEditForm({
  def,
  onSave,
  onCancel,
  saving,
}: {
  def:     DefinitionWithId;
  onSave:  (data: { definition: string; exemple: string | null }) => void;
  onCancel: () => void;
  saving:  boolean;
}) {
  const [definition, setDefinition] = useState(def.definition);
  const [exemple,    setExemple]    = useState(def.exemple ?? "");

  return (
    <div className="space-y-3 rounded-lg border-2 border-orange-300 bg-orange-50 p-3 dark:bg-orange-950">
      <p className="text-xs font-semibold uppercase tracking-wide text-orange-600">
        Modifier la définition #{def.id}
      </p>
      <label className="block">
        <span className="text-xs font-medium text-zinc-600">Définition</span>
        <textarea
          value={definition}
          onChange={(e) => setDefinition(e.target.value)}
          rows={3}
          className="mt-1 w-full rounded-lg border border-zinc-200 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-800"
        />
      </label>
      <label className="block">
        <span className="text-xs font-medium text-zinc-600">Exemple (optionnel)</span>
        <input
          value={exemple}
          onChange={(e) => setExemple(e.target.value)}
          placeholder="ex : …"
          className="mt-1 w-full rounded-lg border border-zinc-200 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-800"
        />
      </label>
      <div className="flex gap-2">
        <Button
          size="sm"
          onClick={() => onSave({ definition, exemple: exemple || null })}
          disabled={saving || !definition.trim()}
        >
          {saving ? "Enregistrement…" : "Enregistrer"}
        </Button>
        <Button size="sm" variant="outline" onClick={onCancel} disabled={saving}>
          Annuler
        </Button>
      </div>
    </div>
  );
}

// ── Composant principal ───────────────────────────────────────────────
export default function AdminMotsPage() {
  const { token } = useAuthStore();

  // Zustand rehydrate depuis localStorage après le premier rendu
  const [hydrated, setHydrated] = useState(false);
  useEffect(() => setHydrated(true), []);
  const tok = hydrated ? token : null;

  // Liste des mots
  const [mots,    setMots]    = useState<Mot[]>([]);
  const [total,   setTotal]   = useState(0);
  const [page,    setPage]    = useState(1);
  const [search,  setSearch]  = useState("");
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState<string | null>(null);

  // Édition mot
  const [editMot,  setEditMot]  = useState<MotDetail | null>(null);
  const [editForm, setEditForm] = useState({ mot_creole: "", phonetique: "", categorie_gram: "", valide: true });
  const [saving,   setSaving]   = useState(false);

  // Panel définitions
  const [defsMot,     setDefsMot]     = useState<Mot | null>(null);
  const [defs,        setDefs]        = useState<DefinitionWithId[]>([]);
  const [defsLoading, setDefsLoading] = useState(false);
  const [defsError,   setDefsError]   = useState<string | null>(null);
  const [editingDef,  setEditingDef]  = useState<DefinitionWithId | null>(null);
  const [defSaving,   setDefSaving]   = useState(false);

  const PAGE_SIZE = 30;

  // ── Chargement mots ──
  const loadMots = useCallback(() => {
    setLoading(true);
    const loader = search.trim()
      ? fastapi.searchWords(search, 50).then((r) => ({ items: r, total: r.length }))
      : fastapi.listWords(page, PAGE_SIZE);
    loader
      .then(({ items, total }) => { setMots(items); setTotal(total); })
      .catch(() => setError("Impossible de charger les mots."))
      .finally(() => setLoading(false));
  }, [page, search]);

  useEffect(() => { loadMots(); }, [loadMots]);

  // ── Édition mot ──
  async function openEditMot(mot: Mot) {
    const detail = await fastapi.getWord(mot.id).catch(() => null);
    if (!detail) return;
    setEditMot(detail);
    setDefsMot(null); // ferme le panel defs si ouvert
    setEditForm({
      mot_creole:     detail.mot_creole,
      phonetique:     detail.phonetique     ?? "",
      categorie_gram: detail.categorie_gram ?? "",
      valide:         detail.valide,
    });
  }

  async function saveMot() {
    if (!editMot || !tok) return;
    setSaving(true);
    try {
      await adminApi.updateMot(tok, editMot.id, {
        mot_creole:     editForm.mot_creole     || undefined,
        phonetique:     editForm.phonetique     || null,
        categorie_gram: editForm.categorie_gram || null,
        valide:         editForm.valide,
      });
      setEditMot(null);
      loadMots();
    } catch (e: unknown) {
      alert((e as Error).message);
    } finally {
      setSaving(false);
    }
  }

  async function deleteMot(id: number) {
    if (!tok || !confirm("Supprimer ce mot et toutes ses définitions ?")) return;
    await adminApi.deleteMot(tok, id).catch((e: unknown) => alert((e as Error).message));
    loadMots();
  }

  // ── Panel définitions ──
  async function openDefs(mot: Mot) {
    if (!tok) return;
    setEditMot(null); // ferme modal édition mot
    setDefsMot(mot);
    setDefs([]);
    setEditingDef(null);
    setDefsError(null);
    setDefsLoading(true);
    try {
      const list = await adminApi.getDefinitions(tok, mot.id);
      setDefs(list);
    } catch (e: unknown) {
      setDefsError((e as Error).message ?? "Erreur lors du chargement.");
    } finally {
      setDefsLoading(false);
    }
  }

  async function saveDef(data: { definition: string; exemple: string | null }) {
    if (!editingDef || !tok || !defsMot) return;
    setDefSaving(true);
    try {
      const updated = await adminApi.updateDefinition(tok, defsMot.id, editingDef.id, data);
      setDefs((prev) => prev.map((d) => (d.id === editingDef.id ? updated : d)));
      setEditingDef(null);
    } catch (e: unknown) {
      alert((e as Error).message);
    } finally {
      setDefSaving(false);
    }
  }

  async function deleteDef(defId: number) {
    if (!tok || !defsMot || !confirm("Supprimer cette définition ?")) return;
    try {
      await adminApi.deleteDefinition(tok, defsMot.id, defId);
      setDefs((prev) => prev.filter((d) => d.id !== defId));
    } catch (e: unknown) {
      alert((e as Error).message);
    }
  }

  // ── Rendu ──────────────────────────────────────────────────────────
  return (
    <div className="space-y-5">
      <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50">
        Mots &amp; Définitions
      </h1>

      {/* Barre de recherche */}
      <div className="flex gap-2">
        <input
          type="text"
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
          placeholder="Rechercher un mot…"
          className="flex-1 rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm shadow-sm outline-none focus:ring-2 focus:ring-orange-400 dark:border-zinc-700 dark:bg-zinc-800"
        />
        {search && (
          <Button variant="outline" size="sm" onClick={() => setSearch("")}>Effacer</Button>
        )}
      </div>

      {loading ? (
        <p className="text-zinc-400">Chargement…</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <>
          <p className="text-xs text-zinc-400">
            {total} mot{total > 1 ? "s" : ""}{search ? ` correspondant à "${search}"` : ""}
          </p>

          <div className="overflow-x-auto rounded-xl border border-zinc-200 dark:border-zinc-700">
            <table className="w-full text-sm">
              <thead className="bg-zinc-50 text-left text-xs uppercase text-zinc-500 dark:bg-zinc-800">
                <tr>
                  <th className="px-4 py-2">ID</th>
                  <th className="px-4 py-2">Mot créole</th>
                  <th className="px-4 py-2">Phonétique</th>
                  <th className="px-4 py-2">Catégorie</th>
                  <th className="px-4 py-2">Valide</th>
                  <th className="px-4 py-2">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
                {mots.map((mot) => (
                  <tr
                    key={mot.id}
                    className={`bg-white hover:bg-zinc-50 dark:bg-zinc-900 dark:hover:bg-zinc-800 ${
                      defsMot?.id === mot.id ? "ring-1 ring-inset ring-orange-300" : ""
                    }`}
                  >
                    <td className="px-4 py-2 font-mono text-xs text-zinc-400">{mot.id}</td>
                    <td className="px-4 py-2 font-medium">{mot.mot_creole}</td>
                    <td className="px-4 py-2 text-zinc-500">{mot.phonetique ?? "—"}</td>
                    <td className="px-4 py-2 text-zinc-500">{mot.categorie_gram ?? "—"}</td>
                    <td className="px-4 py-2">
                      <span className={`rounded-full px-2 py-0.5 text-xs ${mot.valide ? "bg-green-100 text-green-700" : "bg-zinc-100 text-zinc-500"}`}>
                        {mot.valide ? "oui" : "non"}
                      </span>
                    </td>
                    <td className="space-x-1 px-4 py-2">
                      <Button size="sm" variant="outline" onClick={() => openEditMot(mot)}>
                        Éditer
                      </Button>
                      <Button
                        size="sm"
                        variant={defsMot?.id === mot.id ? "default" : "outline"}
                        onClick={() => defsMot?.id === mot.id ? setDefsMot(null) : openDefs(mot)}
                      >
                        Définitions
                      </Button>
                      <Button size="sm" variant="destructive" onClick={() => deleteMot(mot.id)}>
                        Supprimer
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {!search && total > PAGE_SIZE && (
            <div className="flex items-center gap-2">
              <Button size="sm" variant="outline" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
                ← Précédent
              </Button>
              <span className="text-xs text-zinc-500">
                Page {page} / {Math.ceil(total / PAGE_SIZE)}
              </span>
              <Button size="sm" variant="outline" disabled={page >= Math.ceil(total / PAGE_SIZE)} onClick={() => setPage((p) => p + 1)}>
                Suivant →
              </Button>
            </div>
          )}

          {/* ── Panel définitions inline (sous le tableau) ── */}
          {defsMot && (
            <Card className="border-orange-200">
              <CardContent className="pt-4">
                <div className="mb-3 flex items-center justify-between">
                  <h2 className="font-semibold text-zinc-900 dark:text-zinc-50">
                    Définitions — <span className="text-orange-600">{defsMot.mot_creole}</span>
                  </h2>
                  <button onClick={() => { setDefsMot(null); setEditingDef(null); }} className="text-zinc-400 hover:text-zinc-700">✕</button>
                </div>

                {defsLoading && <p className="text-sm text-zinc-400">Chargement…</p>}
                {defsError   && <p className="text-sm text-red-500">{defsError}</p>}

                {!defsLoading && !defsError && (
                  defs.length === 0 ? (
                    <p className="text-sm text-zinc-400">Aucune définition pour ce mot.</p>
                  ) : (
                    <div className="space-y-3">
                      {defs.map((d) => (
                        <div key={d.id}>
                          {editingDef?.id === d.id ? (
                            <DefEditForm
                              def={d}
                              onSave={saveDef}
                              onCancel={() => setEditingDef(null)}
                              saving={defSaving}
                            />
                          ) : (
                            <div className="rounded-lg border border-zinc-100 bg-zinc-50 p-3 dark:border-zinc-800 dark:bg-zinc-800/50">
                              <p className="text-sm text-zinc-800 dark:text-zinc-200">{d.definition}</p>
                              {d.exemple && (
                                <p className="mt-1 text-xs italic text-zinc-500">ex : {d.exemple}</p>
                              )}
                              <div className="mt-2 flex gap-2">
                                <Button
                                  size="sm"
                                  variant="outline"
                                  onClick={() => { setEditingDef(d); }}
                                >
                                  ✏️ Éditer
                                </Button>
                                <Button
                                  size="sm"
                                  variant="destructive"
                                  onClick={() => deleteDef(d.id)}
                                >
                                  Supprimer
                                </Button>
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )
                )}
              </CardContent>
            </Card>
          )}
        </>
      )}

      {/* ── Modal édition mot ── */}
      {editMot && (
        <Modal title={`Éditer « ${editMot.mot_creole} »`} onClose={() => setEditMot(null)}>
          <div className="space-y-3">
            <label className="block">
              <span className="text-xs font-medium text-zinc-600">Mot créole</span>
              <input
                value={editForm.mot_creole}
                onChange={(e) => setEditForm((f) => ({ ...f, mot_creole: e.target.value }))}
                className="mt-1 w-full rounded-lg border border-zinc-200 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-800"
              />
            </label>
            <label className="block">
              <span className="text-xs font-medium text-zinc-600">Phonétique</span>
              <input
                value={editForm.phonetique}
                onChange={(e) => setEditForm((f) => ({ ...f, phonetique: e.target.value }))}
                placeholder="ex : [bɛlɛ]"
                className="mt-1 w-full rounded-lg border border-zinc-200 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-800"
              />
            </label>
            <label className="block">
              <span className="text-xs font-medium text-zinc-600">Catégorie grammaticale</span>
              <select
                value={editForm.categorie_gram}
                onChange={(e) => setEditForm((f) => ({ ...f, categorie_gram: e.target.value }))}
                className="mt-1 w-full rounded-lg border border-zinc-200 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-800"
              >
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>{c || "— non spécifié —"}</option>
                ))}
              </select>
            </label>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={editForm.valide}
                onChange={(e) => setEditForm((f) => ({ ...f, valide: e.target.checked }))}
              />
              Validé
            </label>
            <div className="flex justify-end gap-2 pt-2">
              <Button variant="outline" onClick={() => setEditMot(null)}>Annuler</Button>
              <Button onClick={saveMot} disabled={saving}>
                {saving ? "Enregistrement…" : "Enregistrer"}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}
