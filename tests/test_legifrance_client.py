import pytest
from src.utils.legifrance_client import LegifranceClient
from src.models.schemas import CodeSearchParams, TexteLegalSearchParams, JurisprudenceSearchParams

@pytest.mark.asyncio
async def test_rechercher_code():
    client = LegifranceClient()
    params = CodeSearchParams(
        search="propriété",
        code_name="Code civil",
        page_size=5
    )
    result = await client.rechercher_code(params)
    assert result is not None
    assert "results" in result

@pytest.mark.asyncio
async def test_rechercher_texte_legal():
    client = LegifranceClient()
    params = TexteLegalSearchParams(
        text_id="JORFTEXT000000504704",
        page_size=5
    )
    result = await client.rechercher_texte_legal(params)
    assert result is not None

@pytest.mark.asyncio
async def test_rechercher_jurisprudence():
    client = LegifranceClient()
    params = JurisprudenceSearchParams(
        search="bail commercial",
        page_size=5
    )
    result = await client.rechercher_jurisprudence(params)
    assert result is not None
