import aiohttp

from configreader import config


async def gen_redirect_link(tg_link: str):
    """
    Generate redirect link
    :param tg_link:
    :return:
    """
    headers = {
        'Authorization': f'Bearer {config.redirect_token}'}

    link = f'{config.redirect_base_url}/api/v1/create-or-update?filtersCountryCode=["AU", "AZ", "AL", "DZ", "AS", "VI", "AI", "AO", "AD", "AQ", "AG", "AR", "AW", "AF", "BS", "BD", "BB", "BH", "BZ", "BJ", "BM", "BY", "BO", "BA", "BW", "BR", "IO", "VG", "BN", "BF", "BI", "VU", "VA", "VE", "WF", "VN", "AM", "GA", "HT", "GY", "GM", "GH", "GP", "GT", "GN", "GW", "GG", "HN", "HK", "GD", "GR", "GE", "GU", "GI", "GL", "CD", "JE", "DJ", "DM", "DO", "UM", "EC", "GQ", "ER", "ET", "EG", "YE", "ZM", "EH", "ZW", "IL", "IN", "ID", "IQ", "IR", "JO", "CV", "KZ", "KY", "KH", "CM", "QA", "KE", "KG", "CN", "CY", "KI", "CC", "CO", "KM", "CG", "CR", "CI", "CU", "CW", "LA", "LS", "LR", "LB", "LY", "MU", "MR", "MG", "YT", "MO", "MW", "MY", "ML", "MV", "MT", "MA", "MQ", "MH", "MX", "MZ", "MC", "MN", "MS", "MM", "NA", "NR", "NP", "NE", "NG", "AN", "BQ", "NI", "NU", "NC", "AE", "OM", "BV", "IM", "NF", "CX", "SH", "HM", "CK", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "ZA", "GS", "KR", "SS", "KP", "MK", "MP", "PN", "PT", "PR", "RE", "RU", "PW", "SV", "WS", "SM", "ST", "SA", "SZ", "SJ", "SC", "BL", "SN", "MF", "PM", "VC", "KN", "LC", "RS", "SY", "SG", "SB", "SO", "SD", "SR", "TL", "SL", "TJ", "TH", "TZ", "TC", "TG", "TK", "TO", "TT", "TV", "TN", "TR", "TM", "UG", "UZ", "UY", "FO", "FM", "FJ", "PH", "FK", "GF", "PF", "TF", "CF", "TD", "CL", "ME", "LK", "JM", "JP"]&url={tg_link}'
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as resp:
            if resp.status == 200:
                return await resp.text()

    return False
