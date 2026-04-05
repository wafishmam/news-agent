import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from backend.db.retriever import ingest_articles

SAMPLE_ARTICLES = [
    {
        "id": "art_001",
        "title": "Federal Reserve Raises Interest Rates by 25 Basis Points",
        "date": "2024-11-01",
        "url": "https://example.com/fed-rate-hike-nov-2024",
        "content": (
            "The Federal Reserve announced a 25 basis point increase to the federal funds rate, "
            "bringing it to a range of 5.50-5.75%. Fed Chair Jerome Powell cited persistent inflation "
            "above the 2% target as the primary driver. Markets reacted with moderate volatility, "
            "with the S&P 500 falling 0.8% on the news. Analysts are divided on whether further "
            "hikes are likely before year-end."
        ),
    },
    {
        "id": "art_002",
        "title": "Tech Layoffs Continue as AI Investment Surges",
        "date": "2024-10-15",
        "url": "https://example.com/tech-layoffs-ai-2024",
        "content": (
            "Major technology companies including Meta, Google, and Microsoft announced further "
            "workforce reductions totaling over 12,000 jobs in October, even as capital expenditure "
            "on artificial intelligence infrastructure reached record highs. Analysts say the trend "
            "reflects a structural shift in labor demand rather than financial distress."
        ),
    },
    {
        "id": "art_003",
        "title": "Hurricane Milton Makes Landfall in Florida",
        "date": "2024-10-09",
        "url": "https://example.com/hurricane-milton-landfall",
        "content": (
            "Hurricane Milton made landfall near Siesta Key, Florida as a Category 3 storm with "
            "sustained winds of 120 mph. Over 400,000 residents were under mandatory evacuation orders. "
            "The storm caused widespread flooding across the Tampa Bay area and knocked out power "
            "for more than 1.5 million households. Damage estimates exceed $30 billion."
        ),
    },
    {
        "id": "art_004",
        "title": "OpenAI Launches New Model with Multimodal Reasoning",
        "date": "2024-09-20",
        "url": "https://example.com/openai-model-launch",
        "content": (
            "OpenAI announced the release of its most capable model to date, featuring advanced "
            "multimodal reasoning across text, images, audio, and video. The model achieves "
            "state-of-the-art results on 24 of 25 standard benchmarks. The company also announced "
            "enterprise pricing changes that drew criticism from smaller developers."
        ),
    },
    {
        "id": "art_005",
        "title": "US Economy Added 254,000 Jobs in September",
        "date": "2024-10-04",
        "url": "https://example.com/jobs-report-september-2024",
        "content": (
            "The US economy added 254,000 jobs in September, significantly exceeding analyst "
            "expectations of 140,000. The unemployment rate ticked down to 4.1%. Strong gains "
            "were seen in healthcare, government, and food services. The robust report reduced "
            "expectations for aggressive Federal Reserve rate cuts in the near term."
        ),
    },
    {
        "id": "art_006",
        "title": "Congress Passes Continuing Resolution to Avoid Shutdown",
        "date": "2024-09-27",
        "url": "https://example.com/congress-cr-2024",
        "content": (
            "Congress passed a short-term continuing resolution hours before a government shutdown "
            "deadline, funding federal agencies through mid-November. The resolution does not "
            "include supplemental aid for Ukraine or Israel, punting those debates to the next session."
        ),
    },
    {
        "id": "art_007",
        "title": "California Passes Landmark AI Safety Legislation",
        "date": "2024-09-13",
        "url": "https://example.com/california-ai-safety-bill",
        "content": (
            "California Governor Gavin Newsom signed SB 1047 into law, making California the first "
            "US state to impose broad safety requirements on large AI models. The law requires "
            "developers to implement kill switches and conduct safety evaluations before deploying "
            "models above a certain compute threshold. Critics argue the law will stifle innovation."
        ),
    },
    {
        "id": "art_008",
        "title": "EV Sales Slow as Automakers Adjust Targets",
        "date": "2024-10-22",
        "url": "https://example.com/ev-sales-slowdown-2024",
        "content": (
            "Electric vehicle sales growth slowed significantly in the third quarter of 2024, "
            "prompting Ford and GM to scale back production targets and delay new model launches. "
            "Industry analysts cite high sticker prices, insufficient charging infrastructure, "
            "and consumer range anxiety as key barriers."
        ),
    },
    {
        "id": "art_009",
        "title": "Supreme Court Opens New Term with AI and Copyright Cases",
        "date": "2024-10-01",
        "url": "https://example.com/scotus-term-2024",
        "content": (
            "The Supreme Court opened its new term with a docket heavy on technology and intellectual "
            "property cases, including a landmark suit over whether AI training on copyrighted works "
            "constitutes fair use. Legal observers expect the term to significantly shape the "
            "regulatory landscape for technology companies."
        ),
    },
    {
        "id": "art_010",
        "title": "Israel-Gaza Conflict Enters Second Year",
        "date": "2024-10-07",
        "url": "https://example.com/israel-gaza-one-year",
        "content": (
            "One year after the Hamas-led attacks on October 7, 2023, the conflict in Gaza "
            "continues with no ceasefire in sight. Palestinian health authorities report over "
            "41,000 deaths in Gaza. International mediation efforts by Egypt, Qatar, and the US "
            "have repeatedly stalled over disagreements on hostage release terms."
        ),
    },
]


if __name__ == "__main__":
    print(f"Seeding {len(SAMPLE_ARTICLES)} articles into ChromaDB...")
    count = ingest_articles(SAMPLE_ARTICLES)
    print(f"Done. {count} articles ingested.")