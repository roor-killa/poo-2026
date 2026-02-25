import { getTranslations }           from "next-intl/server";
import { fastapi, type Expression }  from "@/lib/api";
import { Card, CardContent }         from "@/components/ui/card";

export default async function ExpressionsPage() {
  const t = await getTranslations("expressions");

  let items: Expression[] = [];
  try {
    const res = await fastapi.getExpressions(1, 40);
    items     = res.items;
  } catch {}

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-50">{t("title")}</h1>
        <p className="mt-1 text-zinc-500">{t("subtitle")}</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {items.map((ex) => (
          <Card key={ex.id}>
            <CardContent className="pt-4 space-y-1">
              <p className="font-medium text-zinc-800 dark:text-zinc-200">{ex.texte_creole}</p>
              {ex.traduction_fr && (
                <p className="text-sm text-zinc-500">{ex.traduction_fr}</p>
              )}
              {ex.explication && (
                <p className="text-xs text-zinc-400 italic">{ex.explication}</p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
