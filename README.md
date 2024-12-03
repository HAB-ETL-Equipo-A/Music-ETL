# Music-ETL

```bash
git clone https://github.com/HAB-ETL-Equipo-A/Music-ETL
cd Music-ETL
conda create --name music_etl python=3.12
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run home.py
