# -*- coding: utf-8 -*-
import base64, os, html, mimetypes

URL = "hogarelabrazo.ar/sumate"   # PLACEHOLDER: dominio/ruta final de la campaña

def ar(n):
    return "$" + "{:,}".format(int(n)).replace(",", ".")

def datauri(path):
    mt = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mt, base64.b64encode(f.read()).decode())

AMB = [
    ("hermanos", "Cuarto de hermanos"),
    ("banos",    "Baños"),
    ("cocina",   "Cocina y comedor"),
    ("living",   "Living y juegos"),
    ("obra",     "Obra gruesa"),
    ("patio",    "Patio"),
    ("manodeobra","Mano de obra"),
    ("plomeria", "Agua, gas y desagües"),
]

# (amb, escena, precio, estado, dato)
#   estado "libre"   -> dato None
#   estado "parcial" -> dato = recaudado
#   estado "donado"  -> dato = (nombre, fecha)
ITEMS = [
 ("manodeobra","Una semana de los dos obreros",900000,"libre",None),

 ("hermanos","Las dos camas del cuarto de hermanos",640000,"parcial",426000),
 ("hermanos","Dos colchones",360000,"libre",None),
 ("hermanos","El placard del cuarto",185000,"libre",None),
 ("hermanos","La lámpara de la mesa de luz",28000,"donado",("Familia Ferrari","28 jul")),

 ("banos","El termotanque",520000,"parcial",143000),
 ("banos","Los azulejos del baño de los chicos",310000,"libre",None),
 ("banos","La grifería de la ducha",215000,"libre",None),
 ("banos","Un inodoro",148000,"parcial",121000),
 ("banos","El espejo del baño",46000,"donado",("Vero G.","19 jul")),

 ("cocina","La heladera",780000,"parcial",512000),
 ("cocina","El horno",420000,"libre",None),
 ("cocina","La mesa del comedor",340000,"libre",None),
 ("cocina","Ocho sillas",296000,"libre",None),
 ("cocina","La mesada de la cocina",290000,"libre",None),
 ("cocina","Las ollas",84000,"donado",("Silvia y Raúl","11 ago")),

 ("living","El sillón del living",380000,"libre",None),
 ("living","La estufa",240000,"parcial",88000),
 ("living","La biblioteca de los chicos",165000,"libre",None),
 ("living","La mesa para hacer la tarea",78000,"libre",None),
 ("living","Juegos de mesa",34000,"donado",("Los primos","30 jul")),

 ("obra","El tablero eléctrico",470000,"libre",None),
 ("obra","Una ventana",195000,"libre",None),
 ("obra","La pintura de una habitación",135000,"libre",None),
 ("obra","Una puerta con su marco",128000,"libre",None),
 ("obra","Las llaves de luz de una habitación",38000,"donado",("Marce","15 ago")),
 ("obra","Un metro cuadrado de piso",26000,"libre",None),
 ("obra","Un metro de zócalo",11000,"donado",("Anónimo","9 ago")),
 ("obra","Una bolsa de cemento",9000,"libre",None),

 ("patio","La reja del patio",290000,"libre",None),
 ("patio","La hamaca",118000,"parcial",71000),
 ("patio","El pasto del patio",88000,"libre",None),

 # materiales de plomería (lista "materiales hogar.docx"); precios estimados
 ("plomeria","Los caños del agua fría y caliente",390000,"libre",None),
 ("plomeria","Los caños de los desagües",275000,"libre",None),
 ("plomeria","Ramales, curvas y cuplas de los desagües",175000,"libre",None),
 ("plomeria","Las 12 llaves de paso del agua",145000,"libre",None),
 ("plomeria","Las conexiones y llaves del gas",130000,"libre",None),
 ("plomeria","Las salidas para canillas y duchas",115000,"libre",None),
 ("plomeria","Las T y reducciones del agua",90000,"libre",None),
 ("plomeria","Los caños del gas",70000,"libre",None),
 ("plomeria","Codos y curvas del agua",66000,"libre",None),
 ("plomeria","Las cinco piletas de patio",60000,"libre",None),
 ("plomeria","Discos de corte y lubricante",35000,"libre",None),
]

# detalle de materiales que se muestra debajo del título de la tarjeta
DETALLE = {
 "Los caños del agua fría y caliente": "2 caños fusión 50 mm · 10 de 32 mm · 20 de 25 mm",
 "Los caños de los desagües": "7 caños de 110 mm · 6 de 40 mm · 1 de 63 mm",
 "Ramales, curvas y cuplas de los desagües": "9 ramales de 110 mm · 4 curvas 90° 110 mm · 5 cuplas 110 mm · 35 curvas de 40 y 63 mm · 10 reducciones",
 "Las 12 llaves de paso del agua": "12 llaves esféricas fusión 25 mm",
 "Las conexiones y llaves del gas": "3 llaves esféricas 25 mm · 24 codos (4 con rosca) · 5 cuplas · 3 T · 2 reducciones 32 a 25 mm",
 "Las salidas para canillas y duchas": "24 codos 90° 25 mm con rosca hembra · 10 tubos 25 mm con rosca hembra ½",
 "Las T y reducciones del agua": "30 T de 25 mm · 6 T de 50 mm · 16 reducciones · 2 tapones 50 mm",
 "Los caños del gas": "2 tiras de caño fusión 25 mm · 1 tira de 32 mm",
 "Codos y curvas del agua": "60 codos 90° 25 mm · 10 curvas 90° 32 mm · 10 sobrepasos 25 mm",
 "Las cinco piletas de patio": "5 piletas de patio",
 "Discos de corte y lubricante": "5 discos de corte de 110 mm para pared · 4 aerosoles lubricantes",
}

REALES = {"Una semana de los dos obreros"}
LAB = dict(AMB)
CHECK = ('<svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2.5 8.4l3.4 3.4 7.6-7.6" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def card(it):
    amb, scene, price, state, extra = it
    cls = ["item"]
    attrs = ['data-amb="%s"' % amb, 'data-price="%d"' % price, 'data-state="%s"' % state]
    esc = html.escape(scene)
    body = []

    top = ['<span class="amb">%s</span>' % html.escape(LAB[amb])]
    if amb == "hermanos":
        top.append('<span class="badge-h">no los separan</span>')
        cls.append("item-hnos")
    if scene in REALES:
        top.append('<span class="badge-real">dato real</span>')
    body.append('<div class="item-top">%s</div>' % "".join(top))
    body.append('<p class="scene">%s</p>' % esc)
    if scene in DETALLE:
        body.append('<p class="det">%s</p>' % html.escape(DETALLE[scene]))

    if state == "donado":
        cls.append("item-donado")
        name, when = extra
        body.append('<div class="row"><span class="price">%s</span></div>' % ar(price))
        body.append('<div class="foot"><span class="donor">%s Ya está donado</span></div>' % CHECK)
    else:
        if state == "parcial":
            cls.append("item-parcial")
            falta = price - extra
            attrs.append('data-falta="%d"' % falta)
            pct = int(round(extra * 100.0 / price))
            body.append('<div class="rail" role="img" aria-label="%d por ciento reunido"><i style="width:%d%%"></i></div>' % (pct, pct))
            label, sub = "Completar este regalo", '<span class="falta">Faltan %s de %s</span>' % (ar(falta), ar(price))
            pay, concept = falta, "Completar: " + scene
        else:
            label, sub = "Regalar esto", ""
            pay, concept = price, scene

        body.append(
            '<div class="row"><span class="price-block"><span class="price">%s</span>%s</span>'
            '<button class="btn-i" data-open data-concept="%s" data-amount="%d">%s</button></div>'
            % (ar(price), sub, html.escape(concept, quote=True), pay, label))

        if price >= 200000:
            body.append(
                '<div class="foot"><span class="split">Aportá una parte'
                '<button data-open data-concept="%s (25%%)" data-amount="%d">25%%</button>'
                '<button data-open data-concept="%s (50%%)" data-amount="%d">50%%</button></span></div>'
                % (html.escape(scene, quote=True), int(price*.25), html.escape(scene, quote=True), int(price*.5)))
        else:
            body.append('<div class="foot"><span class="split" style="color:var(--ink-3)">Queda a tu nombre en la lista</span></div>')

    return '<article class="%s" %s>%s</article>' % (" ".join(cls), " ".join(attrs), "".join(body))

items_html = "\n      ".join(card(i) for i in ITEMS)

counts = {}
for it in ITEMS:
    counts[it[0]] = counts.get(it[0], 0) + 1
chips = ['<button class="chip" data-amb="todos" aria-pressed="true">Todos <i>%d</i></button>' % len(ITEMS)]
for k, lab in AMB:
    chips.append('<button class="chip" data-amb="%s" aria-pressed="false">%s <i>%d</i></button>'
                 % (k, html.escape(lab), counts.get(k, 0)))
chips_html = "".join(chips)

EQUIPO = [
 ("maria_paz_aznarez",      "María Paz Aznarez",      "Lic. en Trabajo Social",       True),
 ("maria_de_la_paz_iudica", "María de la Paz Iudica", "Lic. en Psicología",           True),
 ("lucia_irigoyen",         "Lucía Irigoyen",         "Lic. en Psicología",           True),
 ("clara_sarandria",        "Clara Sarandría",        "Lic. en Trabajo Social",       False),
 ("carmela_scokin",         "Carmela Scokin",         "Lic. en Economía Empresarial", False),
 ("mauro_duarte",           "Mauro Duarte",           "Téc. Maestro Mayor de Obra",   False),
]
founders_html = "".join(
 '<div class="fnd"><div class="photo"><img src="{{EQ_%s}}" alt="%s" loading="lazy"></div>'
 '<h3>%s</h3><span class="prof">%s</span>%s</div>'
 % (k, html.escape(nm), html.escape(nm), html.escape(pr),
    '<span class="badge-f">Fundadora</span>' if fu else '')
 for k, nm, pr, fu in EQUIPO)

WALL = ["La Grieta","Wenses","Amigas de los Robles","Allaria","Naclerio",
 "Juan Manuel Sosa","Andrea Romanini","Pato Mc Collough","Familia Iudica","Familia Travella",
 "Familia Ruarte","Hospital Austral","JS Carnes","Familia Aguilar","Gonzalo Alonso",
 "Caputo Patricio Constructora","Mauro Duarte","Ferrum"]
names_html = "".join("<span>%s</span>" % html.escape(n) for n in WALL)

FLYER = ""

D = "img/"
IMG = {
 "{{HERO}}":       datauri(D+"hero.jpg"),
 "{{HOY_A}}":      datauri(D+"hoy_a.jpg"),
 "{{RENDER}}":     datauri(D+"render.jpg"),
 "{{EQ_maria_paz_aznarez}}": datauri(D+"eq/maria_paz_aznarez.jpg"),
 "{{EQ_maria_de_la_paz_iudica}}": datauri(D+"eq/maria_de_la_paz_iudica.jpg"),
 "{{EQ_lucia_irigoyen}}": datauri(D+"eq/lucia_irigoyen.jpg"),
 "{{EQ_clara_sarandria}}": datauri(D+"eq/clara_sarandria.jpg"),
 "{{EQ_carmela_scokin}}": datauri(D+"eq/carmela_scokin.jpg"),
 "{{EQ_mauro_duarte}}": datauri(D+"eq/mauro_duarte.jpg"),
 "{{HOY_B}}":      datauri(D+"hoy_b.jpg"),
 "{{LOGO}}":       datauri(D+"logo.png"),
 "{{A_AUSTRAL}}":  datauri(D+"ally_austral.jpg"),
 "{{A_DELLA}}":    datauri(D+"ally_della_vita.jpg"),
 "{{A_MARVAL}}":   datauri(D+"ally_marval.jpg"),
 "{{A_VIAL}}":     datauri(D+"ally_vial.jpg"),
 "{{A_NACLERIO}}": datauri(D+"ally_naclerio.png"),
}

out = (open("tpl_head.html").read() + open("tpl_body.html").read() + open("tpl_js.html").read())
out = out.replace("{{ITEMS}}", items_html).replace("{{CHIPS}}", chips_html)
out = out.replace("{{FOUNDERS}}", founders_html).replace("{{NAMES}}", names_html)
out = out.replace("{{NITEMS}}", str(len(ITEMS))).replace("{{FLYER}}", FLYER).replace("{{URL}}", URL)
for k, v in IMG.items():
    out = out.replace(k, v)

open("abrazo-sumate.html", "w").write(out)
left = [t for t in ("{{", "}}") if t in out]
print("OK  %.0f KB   tokens sin reemplazar: %s   items: %d" % (len(out)/1024.0, left or "ninguno", len(ITEMS)))
