# Hogar El Abrazo — landing de donaciones

Página única de recaudación para la obra del Hogar El Abrazo, en Presidente Derqui, Pilar.
Un hogar convivencial para chicos de 1 a 11 años bajo medida de protección, con prioridad a
los grupos de hermanos para no separarlos.

- Sitio institucional: https://hogarelabrazo.ar
- Instagram: [@elabrazo.hogar](https://www.instagram.com/elabrazo.hogar/)

## Cómo publicarla

`index.html` es la página entera en un solo archivo: las fotos, el logo, el render y los
estilos van embebidos. No necesita servidor, build ni dependencias.

- **Con GitHub Pages:** Settings → Pages → Source: `main` / carpeta raíz. Queda servida en
  `https://<usuario>.github.io/<repo>/`.
- **En un hosting propio:** subir `index.html` y listo.

## Cómo editarla

`index.html` está generado — no se edita a mano. Las fuentes están en `src/`:

| Archivo | Qué tiene |
|---|---|
| `src/tpl_head.html` | Tokens de color, tipografía y todo el CSS |
| `src/tpl_body.html` | El marcado de los once bloques |
| `src/tpl_js.html` | Filtros, orden, modal de pago, QR y el flyer |
| `src/build.py` | La lista de regalos, el equipo, el muro y el armado final |
| `src/img/` | Fotos de obra, render, logo, aliados y equipo |

Para regenerar:

```bash
cd src && python3 build.py
```

Escribe `abrazo-sumate.html`; copiarlo a `index.html` en la raíz.

## Estado de los datos

**Reales:** alias y CVU, los dos links de pago de Mercado Pago, las etapas de obra, el equipo
(fotos y profesiones), los donantes del muro, el logo y el render.

**Todavía estimados:** los precios de la lista de regalos salvo "Una semana de los dos obreros"
($900.000), la rendición de en qué se gastó, y las fechas de las fotos de obra.

## Cobro

Los fondos los administra la Asociación Civil FUPORDEN mientras se tramita la personería
jurídica propia. Por eso el comprobante de pago figura a nombre de FUPORDEN.
