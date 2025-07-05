from datasets import load_dataset
import json

def save_titles_to_json():
    dataset = load_dataset("rcds/wikipedia-persons-masked")
    print("extracting titles from dataset", flush=True)
    titles = list(set(example["title"].replace("_", " ") for example in dataset['train']))
    
    with open("names.json", "w", encoding="utf-8") as f:
        json.dump(titles, f, indent=2)
    
    print(f"saved {len(titles)} titles to titles.json", flush=True)


if __name__ == "__main__":
    save_titles_to_json()
    print("done", flush=True)