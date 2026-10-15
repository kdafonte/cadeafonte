# Ferramentas de arte do Cadê a Fonte

1. `sh tools/setup.sh` — instala fontes (Fraunces, IBM Plex Sans), Chromium headless e dependências.
2. Escreva um `spec.json` (formato no topo de `render.py`) e rode `python3 tools/render.py spec.json`.
3. Os arquivos saem em `posts/<id>/`. Faça commit e push; o link público de cada arquivo é
   `https://raw.githubusercontent.com/kdafonte/cadeafonte/main/posts/<id>/<arquivo>`.

## Identidade

- Fundo `#0E0E0E`, texto `#F4F1EA`, texto secundário `#CFCAC0`, apagado `#8C877E`, destaque amarelo `#FFD21F`.
- Títulos em Fraunces 800/900; corpo em IBM Plex Sans (`font-family: Plex`).
- Todo carrossel termina com o **cartão de prova** (fonte primária, período, nossas contas, data de verificação, código CF-XXXX).
- Toda tela de dado leva um **chip de fonte** no rodapé.

## Componentes — carrossel (1080×1350)

```html
<div class="s">
  <div class="kick">Golpes · em números</div>            <!-- rótulo da editoria -->
  <div class="big">258</div>                             <!-- número gigante (capa) -->
  <div class="h">golpes registrados <em>por hora</em>.</div>  <!-- título; <em> = marca-texto amarelo -->
  <div class="p">Texto de apoio com <b>destaque</b>.</div>
  <div class="chip"><i></i>Fonte · página</div>         <!-- chip de fonte -->
  <div class="foot"><b>cadê a fonte?</b><span>1/7</span><span>@cade.afonte</span></div>
</div>
```

Cartão de prova (última tela):

```html
<div class="s"><div class="stamp">CF-0004</div><div class="kick">Cadê a fonte? Tá aqui.</div>
<div class="proof">
  <div class="row"><div class="l">Fonte primária</div><div class="t">...</div></div>
  <div class="row"><div class="l">Período</div><div class="t">...</div></div>
  <div class="row"><div class="l">Nossas contas</div><div class="t">...</div></div>
  <div class="row"><div class="l">Verificado em</div><div class="t">dd/mm/aaaa</div></div>
</div><div class="foot">...</div></div>
```

Outros: barras (`.bars > .bar > span.y + div(.hi) + span.v`), barras empilhadas
(`.stack > .seg > span.v + div.b.tax|.oth + span`), lista numerada (`ol > li > span + div`).
Use `style="margin-top:120px"` no primeiro `.h` de telas sem número gigante.

## Componentes — Reel e Story (1080×1920)

```html
<div class="r">
  <div class="top">Golpe da falsa central</div>
  <div class="h">Te ligaram da <em>“central do banco”</em>?</div>
  <div class="p">Texto de apoio.</div>
  <div class="bot"><b>cadê a fonte?</b><span>@cade.afonte</span></div>
</div>
```

Reels: 6 a 8 telas, 4 a 7 segundos cada (mais texto = mais tempo), trilha original gerada por `music.py`
embutida no vídeo. A última tela é sempre o cartão de fonte. Não usar áudio do catálogo junto.
