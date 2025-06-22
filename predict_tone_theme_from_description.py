import os
import argparse
import pandas as pd
import openai

def read_text(text_path):
    with open(text_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def import_csv_as_pd(csv_path):
    try:
        return pd.read_csv(csv_path, encoding='cp949')
    except UnicodeDecodeError:
        return pd.read_csv(csv_path, encoding='utf-8')


def get_tone_theme(description):
    prompt = (
        "I want to predict the characteristics of the tracks in this album based on its cover, in order to embed them.\n"
        "Based on the visual elements of the album cover, please predict the emotional tone and narrative theme of the tracks in one sentence each.\n"
        "Each sentence should be in English, short and clear, suitable for CLIP embedding.\n\n"
        "Output exactly two sentences in the format:\n\n"
        "The tone ...\n"
        "The theme ...\n\n"
        f"Description:\n{description}"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {e}"

def modify_df(df):
    df['tone_by_desc'], df['theme_by_desc'] = "", ""
    description_cache = {}

    for idx, row in df.iterrows():
        try:
            description = str(row.get('album_description', '')).strip()
            if not description or description.lower() == 'nan':
                df.at[idx, 'tone_by_desc'] = "N/A"
                df.at[idx, 'theme_by_desc'] = "N/A"
                continue

            if description in description_cache:
                tone, theme = description_cache[description]
            else:
                result = get_tone_theme(description)
                if "The tone" in result and "The theme" in result:
                    parts = result.split("The theme")
                    tone = parts[0].strip()
                    theme = "The theme " + parts[1].strip()
                else:
                    tone, theme = result, ""

                description_cache[description] = (tone, theme)

            df.at[idx, 'tone_by_desc'] = tone
            df.at[idx, 'theme_by_desc'] = theme

        except Exception as e:
            print(f"Error at index {idx}: {e}")
            continue

    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', type=str, required=True)
    parser.add_argument('--csv_path', type=str, required=True)
    parser.add_argument('--out_path', type=str, required=True)
    args = parser.parse_args()

    openai.api_key = read_text(args.key_path)
    
    df = import_csv_as_pd(args.csv_path)
    df = modify_df(df)

    df.to_csv(args.out_path, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()
