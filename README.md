# 🎬 Letterboxd Visualization

**Letterboxd Visualization** é um projeto de **análise de dados** que coleta e visualiza informações de filmes a partir do Letterboxd. Utilizando **Python**, o projeto realiza web scraping para extrair dados de filmes e analisa padrões e tendências nas avaliações.

---

## 📌 **Recursos**
- 🕸️ Coleta automatizada de dados de filmes via web scraping.
- 📊 Análise exploratória dos dados coletados.
- 📈 Visualizações gráficas para identificar padrões e insights.

---

## 📁 **Estrutura do Projeto**
```
📂 LetterboxdVisualization/
│── 📄 README.md               # Documentação do projeto
│── 📄 LetterboxdScrape.py     # Script de scraping de dados do Letterboxd
│── 📄 Data_Gathering.ipynb    # Notebook para coleta de dados
│── 📄 Data_Analysis.ipynb     # Notebook para análise dos dados coletados
│── 📄 test.ipynb              # Notebook de testes e experimentações
```

---

## 🔧 **Instalação e Configuração**
> Recomendado o uso de um ambiente virtual para evitar conflitos de dependências.

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/gabrielcoout/LetterboxdVisualization.git
   cd LetterboxdVisualization
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # No Linux/macOS
   env\Scripts\activate     # No Windows
   ```

3. **Instale as dependências necessárias:**
   ```bash
   pip install -r requirements.txt
   ```

> Se o arquivo `requirements.txt` não estiver disponível, instale manualmente as bibliotecas utilizadas nos notebooks, como `requests`, `beautifulsoup4`, `pandas`, `matplotlib`, entre outras.

---

## 🚀 **Como Usar**
1. **Execute o script de scraping para coletar os dados:**
   ```bash
   python LetterboxdScrape.py
   ```

2. **Abra o notebook de coleta de dados para visualizar e ajustar o processo:**
   - `Data_Gathering.ipynb`

3. **Utilize o notebook de análise para explorar os dados coletados:**
   - `Data_Analysis.ipynb`

4. **Use o notebook de testes para experimentações adicionais:**
   - `test.ipynb`

---

## ✅ **Resultados Esperados**
- Dataset contendo informações detalhadas de filmes do Letterboxd.
- Gráficos e visualizações que destacam tendências e padrões nas avaliações.
- Insights sobre preferências de usuários e características dos filmes.

---

## 📌 **Futuras Melhorias**
- [ ] Implementar scraping de avaliações de usuários específicos.
- [ ] Integrar com APIs externas para enriquecer os dados (ex: TMDb, OMDb).
- [ ] Desenvolver uma interface interativa para visualização dos dados.

---

## 📬 **Contato**
Para dúvidas, sugestões ou contribuições, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

---

*Este projeto é mantido por [@gabrielcoout](https://github.com/gabrielcoout).*
