import json
import pandas as pd

raw = json.load(open("research/trends.json", encoding="utf8"))
g = {k: pd.DataFrame(v).sort_index().astype(float) for k, v in raw.items()}
m1, m2, b1, b2 = g["mu1"], g["mu2"], g["buy1"], g["buy2"]


def z(s):
    return ((s - s.mean()) / s.std()).round(3).tolist()


fortune_month = m1["ดูดวง"].groupby(m1.index.str[5:]).mean().round(1).tolist()
yoy = m2.diff(12).dropna().rolling(3).mean().dropna()
promo = b2.diff().dropna().rolling(3).mean().dropna().tail(48)
shopee = b1.diff().dropna().rolling(3).mean().dropna().tail(48)
rev = b1["รีวิว"]
out = {
    "fortuneMonths": fortune_month,
    "jobFortune": {"a": z(yoy["หางาน"]), "b": z(yoy["ดูดวง"])},
    "reviewPromo": {"a": z(promo["รีวิว"]), "b": z(b2.diff().dropna().rolling(3).mean().dropna().tail(48)["โปรโมชั่น"])},
    "reviewShopee": {"a": z(shopee["รีวิว"]), "b": z(shopee["shopee"])},
    "reviewLine": rev.tolist(),
}
json.dump(out, open("src/charts.json", "w", encoding="utf8"), ensure_ascii=False)
print({k: (len(v) if isinstance(v, list) else len(v["a"])) for k, v in out.items()}, fortune_month[:3])
print("corr shown jobFortune", round(yoy["หางาน"].corr(yoy["ดูดวง"], method="spearman"), 2), "promo", round(promo["รีวิว"].corr(promo["โปรโมชั่น"], method="spearman"), 2), "shopee", round(shopee["รีวิว"].corr(shopee["shopee"], method="spearman"), 2))
