import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.entities import User, Agent, Resource, Offer
from backend.app.core.security import hash_password, hash_token
from backend.app.core.logging import logger

async def seed_demo_data(session: AsyncSession):
    """Seed initial publisher, demo resources, and offers idempotently."""
    # 1. Check if publisher exists
    stmt = select(User).where(User.email == "publisher@paymesh.ai")
    res = await session.execute(stmt)
    publisher = res.scalars().first()
    
    if not publisher:
        publisher = User(
            email="publisher@paymesh.ai",
            password_hash=hash_password("PublisherPass2026!"),
            role="publisher"
        )
        session.add(publisher)
        await session.commit()
        await session.refresh(publisher)
        logger.info("Created demo publisher: publisher@paymesh.ai")

    # 2. Check if buyer agent owner exists
    stmt_buyer = select(User).where(User.email == "buyer@paymesh.ai")
    res_buyer = await session.execute(stmt_buyer)
    buyer = res_buyer.scalars().first()
    if not buyer:
        buyer = User(
            email="buyer@paymesh.ai",
            password_hash=hash_password("BuyerPass2026!"),
            role="buyer"
        )
        session.add(buyer)
        await session.commit()
        await session.refresh(buyer)

        demo_agent = Agent(
            owner_id=buyer.id,
            name="ResearchBot Alpha",
            api_key_hash=hash_token("pm_agent_key_demo_secret_2026"),
            status="active"
        )
        session.add(demo_agent)
        await session.commit()
        logger.info("Created demo buyer agent: ResearchBot Alpha")

    # 3. Seed primary demo resource: Product Intelligence Report (Channel3)
    stmt_res = select(Resource).where(Resource.slug == "product-intelligence-report")
    res_entry = await session.execute(stmt_res)
    pi_resource = res_entry.scalars().first()

    if not pi_resource:
        pi_resource = Resource(
            publisher_id=publisher.id,
            slug="product-intelligence-report",
            title="Channel3 Hardware Intelligence Benchmark",
            description="Deep hardware latency benchmarks, switch tactile profiles, and normalized pricing for high-performance mechanical keyboards.",
            resource_type="product_intelligence",
            provider="channel3",
            metadata_json=json.dumps({
                "category": "electronics",
                "sample_query": "mechanical keyboards",
                "attribution": "Channel3 API normalized product catalog"
            })
        )
        session.add(pi_resource)
        await session.commit()
        await session.refresh(pi_resource)

        offer_1 = Offer(
            resource_id=pi_resource.id,
            offer_code="report_1h",
            title="1-Hour Verified Report Access",
            description="Complete access to latency benchmarks and Channel3 product intelligence.",
            price_amount=0.05,
            currency="USD",
            pricing_model="one_time",
            duration_seconds=3600,
            scope_json=json.dumps({"access": "read", "dataset": "mechanical_keyboards"})
        )
        offer_2 = Offer(
            resource_id=pi_resource.id,
            offer_code="report_24h",
            title="24-Hour Extended Hardware Intelligence Access",
            description="Extended access including all subsequent query refreshes.",
            price_amount=0.15,
            currency="USD",
            pricing_model="one_time",
            duration_seconds=86400,
            scope_json=json.dumps({"access": "read", "dataset": "all_hardware"})
        )
        session.add_all([offer_1, offer_2])
        await session.commit()
        logger.info("Seeded primary demo resource: product-intelligence-report with 2 offers.")

    # 4. Seed legacy news resource for backward compatibility
    stmt_legacy = select(Resource).where(Resource.slug == "legacy-news-feed")
    res_legacy = await session.execute(stmt_legacy)
    legacy_resource = res_legacy.scalars().first()

    if not legacy_resource:
        legacy_resource = Resource(
            publisher_id=publisher.id,
            slug="legacy-news-feed",
            title="CrawlerPal Curated News Feed",
            description="Curated international, technology, and economic news data feed.",
            resource_type="news",
            provider="crawlerpal_demo",
            metadata_json=json.dumps({"category": "general_news"})
        )
        session.add(legacy_resource)
        await session.commit()
        await session.refresh(legacy_resource)

        legacy_offer_1 = Offer(
            resource_id=legacy_resource.id,
            offer_code="one_category",
            title="Access to one category",
            description="Access to all the data in one category",
            price_amount=0.01,
            currency="USD",
            pricing_model="one_time",
            duration_seconds=3600,
            scope_json=json.dumps({"access": "read", "scope": "category"})
        )
        legacy_offer_2 = Offer(
            resource_id=legacy_resource.id,
            offer_code="all_categories",
            title="All Categories Access",
            description="Access all news data in our feed across all categories",
            price_amount=0.05,
            currency="USD",
            pricing_model="one_time",
            duration_seconds=86400,
            scope_json=json.dumps({"access": "read", "scope": "all"})
        )
        session.add_all([legacy_offer_1, legacy_offer_2])
        await session.commit()
        logger.info("Seeded legacy news resource with backward-compatible offers.")
