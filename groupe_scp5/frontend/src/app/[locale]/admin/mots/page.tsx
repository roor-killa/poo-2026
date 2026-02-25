"use client";

import { useEffect, useState, useCallback } from "react";
import { fastapi, adminApi, type Mot, type MotDetail, type DefinitionWithId } from "@/lib/api";
import { useAuthStore } from "@/lib/auth";
import { Button }       from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const CATEGORIES = [
  "", "nom", "vèb", "adjektif", "advèb", "pwonon",
  "prépoziksyon", "konjonksyon", "entèjèksyon", "atik", "lòt",
];

// ── Petit modal réutilisable ──────────────────────────────────────────
function Modal({ title, onClose, children }: {
  title:    string;
  onClose:  () => void;
  children: React.ReactNode;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="w-full max-w-lg rounded-xl bg-white shadow-xl dark:bg-zinc-900">
        <div className="flex items-center justify-between border-b px-5 py-3 dark:border-zinc-700">
          <h2 className="font-semibold text-zinc-900 dark:text-zinc-50">{title}</h2>
          <button
            onClick={onClose}
            className="text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
          >
            ✕
          </button>
        </div>
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}

// ── Composant principal ───────────────────────────────────────────────
export default function AdminMotsPage() {
  const { token } = useAuthStore();

  const [mots,       setMots]       = useState<Mot[]>([]);
  const [total,      setTotal]      = useState(0);
  const [page,       setPage]       = useState(1);
  const [search,     setSearch]     = useState("");
  const [loading,    setLoading]    = useState(true);
  const [error,      setError]      = useState<string | null>(null);

  // Édition d'un mot
  const [editMot,    setEditMot]    = useState<MotDetail | null>(null);
  const [editForm,   setEditForm]   = useState({ mot_creole: "", phonetique: "", categorie_gram: "", valide: true });
  const [saving,     setSaving]     = useState(false);

  // Définitions
  const [defsMotId,  setDefsMotId]  = useState<number | null>(null);
  const [defs,       setDefs]       = useState<DefinitionWithId[]>([]);
  const [editDef,    setEditDef]    = useState<DefinitionWithId | null>(null);
  const [editDefForm,setEditDefForm]= useState({ definition: "", exemple: "" });

  const PAGE_SIZE = 30;

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

  // ── Ouverture édition mot ──
  async function openEditMot(mot: Mot) {
    const detail = await fastapi.getWord(mot.id);
    setEditMot(detail);
    setEditForm({
      mot_creole:     detail.mot_creole,
      phonetique:     detail.phonetique     ?? "",
      categorie_gram: detail.categorie_gram ?? "",
      valide:         detail.valide,
    });
  }

  async function saveMot() {
    if (!editMot || !token) return;
    setSaving(true);
    try {
      await adminApi.updateMot(token, editMot.id, {
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
    if (!token || !confirm("Supprimer ce mot et toutes ses définitions ?")) return;
    await adminApi.deleteMot(token, id);
    loadMots();
  }

  // ── Définitions ──
  async function openDefs(mot: Mot) {
    if (!token) return;
    setDefsMotId(mot.id);
    const list = await adminApi.getDefinitions(token, mot.id);
    setDefs(list);
  }

  function openEditDef(d: DefinitionWithId) {
    setEditDef(d);
    setEditDefForm({ definition: d.definition, exemple: d.exemple ?? "" });
  }

  async function saveDef() {
    if (!editDef || !token || defsMotId === null) return;
    setSaving(true);
    try {
      const updated = await adminApi.updateDefinition(token, defsMotId, editDef.id, {
        definition: editDefForm.definition || undefined,
        exemple:    editDefForm.exemple    || null,
      });
      setDefs((prev) => prev.map((d) => (d.id === editDef.id ? updated : d)));
      setEditDef(null);
    } catch (e: unknown) {
      alert((e as Error).message);
    } finally {
      setSaving(false);
    }
  }

  async function deleteDef(defId: number) {
    if (!token || defsMotId === null || !confirm("Supprimer cette définition ?")) return;
    await adminApi.deleteDefinition(token, defsMotId, defId);
    setDefs((prev) => prev.filter((d) => d.id !== defId));
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
          <Button variant="outline" size="sm" onClick={() => setSearch("")}>
            Effacer
          </Button>
        )}
      </div>

      {/* Tableau */}
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
                    className="bg-white hover:bg-zinc-50 dark:bg-zinc-900 dark:hover:bg-zinc-800"
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
                      <Button size="sm" variant="outline" onClick={() => openDefs(mot)}>
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
              <Button
                size="sm"
                variant="outline"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                ← Précédent
              </Button>
              <span className="text-xs text-zinc-500">
                Page {page} / {Math.ceil(total / PAGE_SIZE)}
              </span>
              <Button
                size="sm"
                variant="outline"
                disabled={page >= Math.ceil(total / PAGE_SIZE)}
                onClick={() => setPage((p) => p + 1)}
              >
                Suivant →
              </Button>
            </div>
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

      {/* ── Panel définitions ── */}
      {defsMotId !== null && (
        <Modal
          title={`Définitions — mot #${defsMotId}`}
          onClose={() => { setDefsMotId(null); setEditDef(null); }}
        >
          {defs.length === 0 ? (
            <p className="text-sm text-zinc-400">Aucune définition.</p>
          ) : (
            <div className="space-y-3">
              {defs.map((d) =>
                editDef?.id === d.id ? (
                  <Card key={d.id} className="border-orange-200">
                    <CardContent className="space-y-2 pt-3">
                      <textarea
                        value={editDefForm.definition}
                        onChange={(e) => setEditDefForm((f) => ({ ...f, definition: e.target.value }))}
                        rows={3}
                        className="w-full rounded border border-zinc-200 px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-800"
                      />
                      <input
                        value={editDefForm.exemple}
                        onChange={(e) => setEditDefForm((f) => ({ ...f, exemple: e.target.value }))}
                        placeholder="Exemple (optionnel)"
                        className="w-full rounded border border-zinc-200 px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-800"
                      />
                      <div className="flex gap-2">
                        <Button size="sm" onClick={saveDef} disabled={saving}>
                          {saving ? "…" : "Enregistrer"}
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => setEditDef(null)}>
                          Annuler
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ) : (
                  <Card key={d.id}>
                    <CardContent className="pt-3">
                      <p className="text-sm">{d.definition}</p>
                      {d.exemple && (
                        <p className="mt-1 text-xs italic text-zinc-400">ex : {d.exemple}</p>
                      )}
                      <div className="mt-2 flex gap-2">
                        <Button size="sm" variant="outline" onClick={() => openEditDef(d)}>
                          Éditer
                        </Button>
                        <Button size="sm" variant="destructive" onClick={() => deleteDef(d.id)}>
                          Supprimer
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )
              )}
            </div>
          )}
        </Modal>
      )}
    </div>
  );
}
