#!/usr/bin/env python
"""Generate bundled SQuAD fallback data."""
import json
from pathlib import Path

ARTICLES = [
    {
        "title": "George Washington",
        "context": (
            "George Washington (February 22, 1732 – December 14, 1799) was an American "
            "Founding Father, military officer, and politician who served as the first "
            "president of the United States from 1789 to 1797. Appointed by the Continental "
            "Congress as commander of the Continental Army, Washington led the Patriot forces "
            "to victory in the American Revolutionary War and served as president of the "
            "Constitutional Convention in 1787, which drafted the current Constitution of "
            "the United States. Washington has been called the Father of the Nation for his "
            "manifold leadership in the formative days of the country. Washington was born on "
            "February 22, 1732, at Popes Creek in Westmoreland County, Virginia. He was raised "
            "in colonial Virginia and became a surveyor. He inherited Mount Vernon and married "
            "Martha Dandridge Custis. During the American Revolution, Washington commanded the "
            "Continental Army from 1775 to 1783. After the war he resigned his commission and "
            "retired to Mount Vernon."
        ),
        "qas": [
            ("When was George Washington born?", "February 22, 1732"),
            ("What was George Washington's role in the American Revolution?", "commander of the Continental Army"),
            ("When did Washington serve as president?", "1789 to 1797"),
            ("Where was George Washington born?", "Popes Creek in Westmoreland County, Virginia"),
            ("What estate did Washington inherit?", "Mount Vernon"),
            ("Who did Washington marry?", "Martha Dandridge Custis"),
            ("When did Washington command the Continental Army?", "1775 to 1783"),
            ("What convention did Washington preside over in 1787?", "Constitutional Convention"),
            ("What title has Washington been given?", "Father of the Nation"),
            ("When did George Washington die?", "December 14, 1799"),
        ],
    },
    {
        "title": "France",
        "context": (
            "France, officially the French Republic, is a country located primarily in Western "
            "Europe. Its metropolitan area extends from the Rhine to the Atlantic Ocean and from "
            "the Mediterranean Sea to the English Channel and the North Sea. France borders "
            "Belgium, Luxembourg, Germany, Switzerland, Monaco, Italy, Andorra, and Spain. Its "
            "overseas territories include French Guiana in South America and several islands in "
            "the Atlantic, Pacific, and Indian Oceans. France has a population of about 68 million "
            "and its capital and largest city is Paris. French is the official language. France "
            "is a unitary semi-presidential republic. The current president is Emmanuel Macron. "
            "France is a founding member of the European Union and a permanent member of the "
            "United Nations Security Council."
        ),
        "qas": [
            ("What is the capital of France?", "Paris"),
            ("What is the official language of France?", "French"),
            ("What is France's population approximately?", "68 million"),
            ("Who is the current president of France?", "Emmanuel Macron"),
            ("What type of government does France have?", "unitary semi-presidential republic"),
            ("Which ocean borders France to the west?", "Atlantic Ocean"),
            ("Which country borders France to the northeast?", "Belgium"),
            ("What sea is to the south of France?", "Mediterranean Sea"),
            ("Is France a member of the European Union?", "founding member"),
            ("What is France's full official name?", "French Republic"),
        ],
    },
    {
        "title": "William Shakespeare",
        "context": (
            "William Shakespeare (baptised 26 April 1564 – 23 April 1616) was an English "
            "playwright, poet and actor. He is widely regarded as the greatest writer in the "
            "English language and the world's pre-eminent dramatist. Shakespeare produced most "
            "of his known works between 1589 and 1613. His early plays were primarily comedies "
            "and histories. He then wrote mainly tragedies until 1608, including Hamlet, Othello, "
            "King Lear, and Macbeth. In the last phase of his life he wrote tragicomedies and "
            "collaborated with other playwrights. Shakespeare wrote Romeo and Juliet, a tragedy "
            "about two young star-crossed lovers. He was born and raised in Stratford-upon-Avon, "
            "Warwickshire. Shakespeare married Anne Hathaway at age 18. He died on 23 April 1616 "
            "at the age of 52."
        ),
        "qas": [
            ("Who wrote Romeo and Juliet?", "William Shakespeare"),
            ("Where was Shakespeare born?", "Stratford-upon-Avon"),
            ("When did Shakespeare die?", "23 April 1616"),
            ("Who did Shakespeare marry?", "Anne Hathaway"),
            ("Name a Shakespeare tragedy.", "Hamlet"),
            ("What was Shakespeare's profession?", "playwright, poet and actor"),
            ("When was Shakespeare baptised?", "26 April 1564"),
            ("What type of play is Romeo and Juliet?", "tragedy"),
            ("In which county was Shakespeare born?", "Warwickshire"),
            ("During what period did Shakespeare write most works?", "1589 and 1613"),
        ],
    },
    {
        "title": "Python (programming language)",
        "context": (
            "Python is a high-level, general-purpose programming language. Its design philosophy "
            "emphasizes code readability with the use of significant indentation. Python is "
            "dynamically typed and garbage-collected. It supports multiple programming paradigms, "
            "including structured, object-oriented and functional programming. Python was "
            "conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica "
            "(CWI) in the Netherlands. Python 2.0 was released in 2000. Python 3.0, a major "
            "revision, was released in 2008. Python consistently ranks as one of the most popular "
            "programming languages. The Python Package Index (PyPI) hosts thousands of third-party "
            "modules. Python is widely used in data science, web development, automation, and "
            "artificial intelligence."
        ),
        "qas": [
            ("Who created Python?", "Guido van Rossum"),
            ("Where was Python conceived?", "Centrum Wiskunde & Informatica (CWI) in the Netherlands"),
            ("When was Python 3.0 released?", "2008"),
            ("What does Python emphasize in its design?", "code readability"),
            ("What is PyPI?", "Python Package Index"),
            ("Is Python dynamically typed?", "dynamically typed"),
            ("When was Python 2.0 released?", "2000"),
            ("What paradigms does Python support?", "structured, object-oriented and functional programming"),
            ("In what fields is Python widely used?", "data science, web development, automation, and artificial intelligence"),
            ("What type of language is Python?", "high-level, general-purpose programming language"),
        ],
    },
    {
        "title": "World War II",
        "context": (
            "World War II or the Second World War (1939–1945) was a global conflict involving "
            "most of the world's nations. It was the deadliest conflict in human history. The war "
            "began on 1 September 1939 when Germany invaded Poland. The two main opposing military "
            "alliances were the Allies and the Axis powers. Key Allied leaders included Franklin "
            "D. Roosevelt, Winston Churchill, and Joseph Stalin. Adolf Hitler led Nazi Germany, "
            "the primary Axis power in Europe. The war in Europe ended with the German surrender "
            "on 8 May 1945 (VE Day). The war in the Pacific ended after atomic bombs were dropped "
            "on Hiroshima and Nagasaki in August 1945, leading to Japan's surrender on 2 September "
            "1945 (VJ Day). An estimated 70 to 85 million people died in the conflict."
        ),
        "qas": [
            ("When did World War II begin?", "1939"),
            ("What event started World War II in Europe?", "Germany invaded Poland"),
            ("When did Germany invade Poland?", "1 September 1939"),
            ("Who was the leader of Nazi Germany?", "Adolf Hitler"),
            ("What were the two main alliances?", "Allies and the Axis powers"),
            ("When did the war in Europe end?", "8 May 1945"),
            ("What cities were atomic bombs dropped on?", "Hiroshima and Nagasaki"),
            ("Who was the British Prime Minister during WWII?", "Winston Churchill"),
            ("When did World War II end?", "1945"),
            ("How many people died in World War II approximately?", "70 to 85 million"),
        ],
    },
]


def main():
    squad = {"version": "v2.0", "data": []}
    articles_dir = Path(__file__).parent.parent / "data" / "fallback" / "articles"
    articles_dir.mkdir(parents=True, exist_ok=True)

    for art in ARTICLES:
        qas = []
        for i, (question, answer) in enumerate(art["qas"]):
            start = art["context"].find(answer)
            qas.append(
                {
                    "id": f"{art['title'].replace(' ', '_').replace('(', '').replace(')', '')}_{i}",
                    "question": question,
                    "answers": [{"text": answer, "answer_start": max(start, 0)}],
                    "is_impossible": False,
                }
            )
        squad["data"].append({"title": art["title"], "paragraphs": [{"context": art["context"], "qas": qas}]})

        safe_name = art["title"].lower().replace(" ", "_").replace("(", "").replace(")", "")
        (articles_dir / f"{safe_name}.txt").write_text(art["context"], encoding="utf-8")

    out = Path(__file__).parent.parent / "data" / "fallback" / "squad_sample.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(squad, f, indent=2)

    n_qas = sum(len(p["qas"]) for a in squad["data"] for p in a["paragraphs"])
    print(f"Created {out} with {len(squad['data'])} articles and {n_qas} QA pairs")


if __name__ == "__main__":
    main()
