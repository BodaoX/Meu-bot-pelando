# pelando_bot

bot de scraping em python para monitorar ofertas do site pelando  
https://www.pelando.com.br

o projeto foi **100% refatorado e repensado**, focando em:

- simplicidade
- estabilidade
- baixo consumo
- evitar duplicações
- respeito a intervalos de verificação

---

## visão geral

o `pelando_bot` acessa a página de ofertas recentes do pelando, identifica novas promoções, extrai informações detalhadas de cada oferta e envia apenas ofertas relevantes para o discord.

o bot mantém um histórico local em sqlite para:

- evitar envio duplicado
- detectar mudança de preço
- reenviar apenas se o preço diminuir

---

## principais funcionalidades

- scraping da página `/recentes` do pelando
- leitura estruturada via `feed-schema` (json-ld)
- extração detalhada de cada oferta:
  - título
  - preço
  - imagem
  - link
  - cupom (quando existir)
- normalização de texto (acentos e encoding)
- formatação correta de preço brasileiro (ex: `1.299,00`)
- persistência em sqlite
- envio de ofertas para discord via webhook
- verificação periódica configurável (ex: a cada 1s, 30s, 5min)

---

## requisitos

- python 3.9 ou superior
- bibliotecas python:
  - requests
  - beautifulsoup4

---

## instalação

instale as dependências com:

```bash
pip install -r requirements.txt
```
