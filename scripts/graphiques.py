import csv, json, html, subprocess, math
BG="#0f172a"; INK="#e2e8f0"; MUTED="#94a3b8"; GRID="#1e293b"; BLUE="#60a5fa"; PINK="#f472b6"; AMB="#fbbf24"
FONT='font-family="system-ui,-apple-system,Segoe UI,Roboto,sans-serif"'
def head(w,h,title,sub):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(title)}" {FONT}>',
            f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>',
            f'<text x="28" y="40" fill="{INK}" font-size="20" font-weight="700">{html.escape(title)}</text>',
            f'<text x="28" y="64" fill="{MUTED}" font-size="14">{html.escape(sub)}</text>']
def save(name,o):
    o.append('</svg>'); p=f"img/{name}.svg"; open(p,"w").write("\n".join(o))
    subprocess.run(["rsvg-convert","-w","900","-o",f"img/{name}.png",p],check=True)
SRC="Sources : Géovélo (oct. 2026), FUB Baromètre 2025, Insee RP, calculs xj1.fr"

# --- 1. scatter national
rows=list(csv.DictReader(open("scatter.csv")))
w,h=900,580; L,R,T,B=70,30,86,92
X0,X1,Y0,Y1=0,6,1.8,4.8
def sx(v): return L+(w-L-R)*min(v,X1)/(X1-X0)
def sy(v): return T+(h-T-B)*(1-(v-Y0)/(Y1-Y0))
o=head(w,h,"Plus de pistes, meilleure note ? Un lien réel, mais lâche","2 626 communes notées par la FUB en 2025 : kilomètres d'aménagements pour 1 000 habitants et note globale (sur 5)")
for v in (2,3,4):
    o.append(f'<line x1="{L}" x2="{w-R}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{GRID}"/>')
    o.append(f'<text x="{L-10}" y="{sy(v)+5:.1f}" fill="{MUTED}" font-size="13" text-anchor="end">{v}</text>')
for v in range(0,7):
    o.append(f'<line y1="{T}" y2="{h-B}" x1="{sx(v):.1f}" x2="{sx(v):.1f}" stroke="{GRID}"/>')
    o.append(f'<text x="{sx(v):.1f}" y="{h-B+22}" fill="{MUTED}" font-size="13" text-anchor="middle">{v}{"+" if v==6 else ""}</text>')
o.append(f'<text x="{(L+w-R)/2}" y="{h-B+44}" fill="{MUTED}" font-size="14" text-anchor="middle">km d’aménagements cyclables pour 1 000 habitants</text>')
o.append(f'<text x="18" y="{(T+h-B)/2}" fill="{MUTED}" font-size="14" text-anchor="middle" transform="rotate(-90 18 {(T+h-B)/2})">note FUB 2025</text>')
for r in rows:
    k=float(r["km1000"]); s=float(r["score"])
    o.append(f'<circle cx="{sx(k):.0f}" cy="{sy(s):.0f}" r="2.4" fill="{BLUE}" fill-opacity=".35"/>')
lab={"Grenoble":(8,-8),"Strasbourg":(8,-8),"La Rochelle":(8,-6),"Nice":(8,14),"Arles":(8,16),"Illzach":(8,16),"Cambrai":(8,16),"Rennes":(-9,18),"Mèze":(-8,-8)}
for r in rows:
    n=r["nom"]
    if n in lab and float(r["pop"])>10000:
        k=float(r["km1000"]); s=float(r["score"]); dx,dy=lab[n]
        o.append(f'<circle cx="{sx(k):.0f}" cy="{sy(s):.0f}" r="5" fill="{AMB}" stroke="{BG}" stroke-width="1.5"/>')
        o.append(f'<text x="{sx(k)+dx:.0f}" y="{sy(s)+dy:.0f}" fill="{INK}" font-size="13" font-weight="700" text-anchor="{"end" if dx<0 else "start"}">{html.escape(n)}</text>')
o.append(f'<text x="28" y="{h-12}" fill="{MUTED}" font-size="13">Corrélation 0,38. {SRC}</text>')
save("velo-scatter",o)

# --- 2. quartiles
q=[("Quart le moins équipé (0,4 km en médiane)",1.40),("2e quart (1,1 km en médiane)",2.03),("3e quart (1,9 km en médiane)",2.71),("Quart le plus équipé (3,5 km en médiane)",3.05)]
w=900; lm=330; rm=90; top=92; rh=44; h=top+len(q)*rh+54
o=head(w,h,"Neuf fois plus de kilomètres, deux fois plus de cyclistes","Actifs allant au travail à vélo (médiane), communes de 5 000 hab. et plus, par quart de km/1 000 hab.")
plot=w-lm-rm; y=top
for lab_,v in q:
    bw=plot*v/4
    o.append(f'<text x="{lm-12}" y="{y+22}" fill="{INK}" font-size="14" text-anchor="end">{html.escape(lab_)}</text>')
    o.append(f'<rect x="{lm}" y="{y+6}" width="{bw:.1f}" height="22" rx="5" fill="{BLUE}"/>')
    o.append(f'<text x="{lm+bw+8:.1f}" y="{y+23}" fill="{INK}" font-size="15" font-weight="700">{str(v).replace(".",",")} %</text>')
    y+=rh
o.append(f'<text x="28" y="{h-18}" fill="{MUTED}" font-size="13">2 143 communes. {SRC}</text>')
save("velo-quartiles",o)

# --- 3. Paris west -> east
P=sorted(json.load(open("paris_arr.json")),key=lambda a:a["lon"])
w=900; lm=70; rm=210; top=92; rh=27; h=top+len(P)*rh+58
o=head(w,h,"À Paris, les cyclistes de l’ouest sont moins satisfaits que ceux de l’est","Note moyenne des cyclistes par arrondissement (Baromètre FUB 2025), de l’ouest (en haut) à l’est (en bas). À droite : km d’aménagements dédiés, réponses")
plot=w-lm-rm; y=top
vmin,vmax=2.5,3.8
for i,a in enumerate(P):
    col=PINK if i<10 else BLUE
    bw=plot*(a["fub_score"]-vmin)/(vmax-vmin)
    o.append(f'<text x="{lm-10}" y="{y+17}" fill="{INK}" font-size="14" text-anchor="end">{a["arr"]}{"er" if a["arr"]==1 else "e"}</text>')
    o.append(f'<rect x="{lm}" y="{y+4}" width="{bw:.1f}" height="16" rx="4" fill="{col}"><title>{a["arr"]}e : note {a["fub_score"]}, {a["km_ded"]} km d’aménagements dédiés, {a["fub_n"]} réponses</title></rect>')
    o.append(f'<text x="{lm+bw+8:.1f}" y="{y+17}" fill="{INK}" font-size="14" font-weight="700">{str(a["fub_score"]).replace(".",",")}</text>')
    o.append(f'<text x="{w-28}" y="{y+17}" fill="{MUTED}" font-size="13" text-anchor="end">{a["km_ded"]:.0f} km · {a["fub_n"]} rép.</text>'.replace(".0 km"," km"))
    y+=rh
o.append(f'<text x="{lm}" y="{h-30}" fill="{PINK}" font-size="13">■ 10 arrondissements les plus à l’ouest</text>')
o.append(f'<text x="{lm+300}" y="{h-30}" fill="{BLUE}" font-size="13">■ 10 les plus à l’est</text>')
o.append(f'<text x="28" y="{h-10}" fill="{MUTED}" font-size="13">Moyenne brute des réponses, axe tronqué à 2,5. Ville de Paris (oct. 2026), FUB 2025, calculs xj1.fr</text>')
save("velo-paris-est-ouest",o)
