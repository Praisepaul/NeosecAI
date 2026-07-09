import { monitoredProducts } from "@/data/products";
import { threatFeed } from "@/data/threatIntel";

export function getRelevantThreats() {
  return threatFeed.filter((threat) =>
    threat.affectedProducts.some((product) =>
      monitoredProducts.includes(product)
    )
  );
}