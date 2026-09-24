from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime
import json
import re
import time
from urllib.parse import urlparse

HOT_URL = "https://hotcorphml.globalhitss.com.br/index/"
HOT_HOST = urlparse(HOT_URL).hostname or ""

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "mapeamentos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SELECTOR = """
button,
input,
select,
textarea,
a,
form,
nav,
iframe,
[role],
[data-testid],
[data-test],
[data-qa],
[data-cy],
[aria-label],
[title],
[contenteditable="true"]
"""

ATTRIBUTES = [
    "id", "name", "type", "role", "placeholder",
    "aria-label", "aria-labelledby", "aria-describedby",
    "title", "data-testid", "data-test", "data-qa",
    "data-cy", "href", "class", "for", "autocomplete",
    "disabled", "readonly", "required", "tabindex",
]


def slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "pagina"


def compact(value, limit=250):
    if value is None:
        return None
    value = re.sub(r"\s+", " ", str(value)).strip()
    if not value:
        return None
    return value[:limit] + "..." if len(value) > limit else value


def safe_attr(locator, name):
    try:
        return compact(locator.get_attribute(name))
    except Exception:
        return None


def safe_text(locator):
    try:
        return compact(locator.inner_text(timeout=400))
    except Exception:
        return None


def safe_label(locator):
    try:
        value = locator.evaluate(
            """
            e => {
                if (!e.labels || e.labels.length === 0) return null;
                return Array.from(e.labels)
                    .map(label => (label.innerText || label.textContent || "").trim())
                    .filter(Boolean)
                    .join(" | ");
            }
            """
        )
        return compact(value)
    except Exception:
        return None


def safe_select_options(locator):
    try:
        tag = locator.evaluate("e => e.tagName.toLowerCase()")
        if tag != "select":
            return None
        return locator.evaluate(
            """
            e => Array.from(e.options).map(o => ({
                text: (o.textContent || "").trim(),
                value: o.value
            }))
            """
        )
    except Exception:
        return None


def is_sensitive_or_internal(attributes, frame_url):
    element_type = (attributes.get("type") or "").lower()
    name = (attributes.get("name") or "").lower()
    element_id = (attributes.get("id") or "").lower()
    frame_url_lower = (frame_url or "").lower()

    markers = (
        "csrf", "recaptcha", "g-recaptcha", "token",
        "password", "passwd", "secret",
    )

    if element_type in {"password", "hidden"}:
        return True

    combined = f"{name} {element_id} {frame_url_lower}"
    return any(marker in combined for marker in markers)


def safe_accessible_name(locator, label=None):
    if label:
        return label
    for attr in ("aria-label", "title", "placeholder"):
        value = safe_attr(locator, attr)
        if value:
            return value
    return safe_text(locator)


def css_escape_value(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def build_candidates(item):
    a = item["attributes"]
    result = []

    def add(priority, type_, locator, strategy, value=None, role=None, name=None):
        result.append({
            "priority": priority,
            "type": type_,
            "locator": locator,
            "strategy": strategy,
            "value": value,
            "role": role,
            "name": name,
            "matches": None,
            "unique": None,
            "recommended": False,
        })

    for field in ("data-testid", "data-test", "data-qa", "data-cy"):
        if a.get(field):
            escaped = css_escape_value(a[field])
            selector = f'[{field}="{escaped}"]'
            add(1, field, selector, "css", value=selector)

    if a.get("role") and item.get("accessible_name"):
        add(
            2,
            "role+name",
            f'role={a["role"]}[name="{item["accessible_name"]}"]',
            "role",
            role=a["role"],
            name=item["accessible_name"],
        )

    if item.get("label"):
        add(2, "label", f'label="{item["label"]}"', "label", value=item["label"])

    if a.get("aria-label"):
        escaped = css_escape_value(a["aria-label"])
        selector = f'[aria-label="{escaped}"]'
        add(2, "aria-label", selector, "css", value=selector)

    if a.get("id"):
        escaped = css_escape_value(a["id"])
        display_locator = f'#{a["id"]}'
        selector = f'[id="{escaped}"]'
        add(3, "id", display_locator, "css", value=selector)

    if a.get("name"):
        escaped = css_escape_value(a["name"])
        selector = f'[name="{escaped}"]'
        add(4, "name", selector, "css", value=selector)

    if a.get("href") and a.get("href") not in {"#", "javascript:void(0)", "javascript:void(0);"}:
        escaped = css_escape_value(a["href"])
        selector = f'[href="{escaped}"]'
        add(4, "href", selector, "css", value=selector)

    if a.get("placeholder"):
        add(
            5,
            "placeholder",
            f'placeholder="{a["placeholder"]}"',
            "placeholder",
            value=a["placeholder"],
        )

    if item.get("text") and len(item["text"]) <= 120:
        add(6, "text", f'text="{item["text"]}"', "text", value=item["text"])

    return result


def count_candidate_matches(frame, candidate):
    try:
        strategy = candidate["strategy"]
        if strategy == "css":
            return frame.locator(candidate["value"]).count()
        if strategy == "role":
            return frame.get_by_role(candidate["role"], name=candidate["name"], exact=True).count()
        if strategy == "label":
            return frame.get_by_label(candidate["value"], exact=True).count()
        if strategy == "placeholder":
            return frame.get_by_placeholder(candidate["value"], exact=True).count()
        if strategy == "text":
            return frame.get_by_text(candidate["value"], exact=True).count()
    except Exception:
        return None
    return None


def evaluate_candidates(frame, item):
    candidates = build_candidates(item)

    for candidate in candidates:
        matches = count_candidate_matches(frame, candidate)
        candidate["matches"] = matches
        candidate["unique"] = matches == 1

        if item["sensitive_or_internal"]:
            continue

        candidate["recommended"] = bool(
            candidate["unique"]
            and candidate["priority"] <= 5
            and candidate["type"] != "text"
        )

    recommended = [c for c in candidates if c.get("recommended")]
    recommended.sort(key=lambda c: c["priority"])

    item["locator_candidates"] = candidates
    item["recommended_locator"] = recommended[0]["locator"] if recommended else None


def collect_element(frame, locator, index, frame_index, frame_url):
    try:
        base = locator.evaluate(
            """
            e => {
                const r = e.getBoundingClientRect();
                const style = window.getComputedStyle(e);
                const visible =
                    style.display !== "none" &&
                    style.visibility !== "hidden" &&
                    style.opacity !== "0" &&
                    !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
                return {
                    tag: e.tagName,
                    visible,
                    enabled: !e.disabled,
                    checked: typeof e.checked === "boolean" ? e.checked : null,
                    selected: typeof e.selected === "boolean" ? e.selected : null,
                    required: !!e.required,
                    readOnly: !!e.readOnly,
                    x: Math.round(r.x),
                    y: Math.round(r.y),
                    width: Math.round(r.width),
                    height: Math.round(r.height)
                };
            }
            """
        )
    except Exception:
        return None

    attributes = {attr: safe_attr(locator, attr) for attr in ATTRIBUTES}
    label = safe_label(locator)
    sensitive = is_sensitive_or_internal(attributes, frame_url)

    item = {
        "index": index,
        "frame_index": frame_index,
        "frame_url": frame_url,
        "tag": base.get("tag"),
        "visible": base.get("visible"),
        "enabled": base.get("enabled"),
        "checked": base.get("checked"),
        "selected": base.get("selected"),
        "required": base.get("required"),
        "read_only": base.get("readOnly"),
        "position": {
            "x": base.get("x"),
            "y": base.get("y"),
            "width": base.get("width"),
            "height": base.get("height"),
        },
        "text": None if sensitive else safe_text(locator),
        "label": label,
        "accessible_name": None if sensitive else safe_accessible_name(locator, label),
        "attributes": attributes,
        "select_options": None if sensitive else safe_select_options(locator),
        "sensitive_or_internal": sensitive,
        "locator_candidates": [],
        "recommended_locator": None,
    }

    evaluate_candidates(frame, item)
    return item


def page_relevant_count(page):
    if page is None or page.is_closed():
        return -1
    try:
        return page.locator(SELECTOR).count()
    except Exception:
        return -1


def page_score(page):
    if page is None or page.is_closed():
        return -999999

    try:
        url = page.url or ""
    except Exception:
        url = ""

    score = 0

    if url and url != "about:blank":
        score += 100

    try:
        host = urlparse(url).hostname or ""
        if host == HOT_HOST:
            score += 1000
    except Exception:
        pass

    score += max(page_relevant_count(page), 0)
    return score


def get_active_page(context):
    alive = [page for page in context.pages if not page.is_closed()]
    if not alive:
        return None
    return max(
        enumerate(alive),
        key=lambda pair: (page_score(pair[1]), pair[0])
    )[1]


def wait_for_page_ready(context, timeout_seconds=15):
    end = time.time() + timeout_seconds
    best_page = None
    best_count = -1

    while time.time() < end:
        page = get_active_page(context)

        if page is not None:
            count = page_relevant_count(page)

            if count > best_count:
                best_count = count
                best_page = page

            if count > 0:
                try:
                    page.wait_for_load_state("domcontentloaded", timeout=2000)
                except Exception:
                    pass
                time.sleep(0.6)
                return page

        time.sleep(0.4)

    return best_page


def collect_page(page):
    all_elements = []
    frames_meta = []

    for frame_index, frame in enumerate(page.frames):
        try:
            locator = frame.locator(SELECTOR)
            total = locator.count()
        except Exception:
            total = 0

        frame_elements = []

        for index in range(total):
            try:
                item = collect_element(frame, locator.nth(index), index, frame_index, frame.url)
                if item:
                    frame_elements.append(item)
            except Exception as exc:
                print(f"[AVISO] frame={frame_index} elemento={index}: {exc}")

        all_elements.extend(frame_elements)
        frames_meta.append({
            "frame_index": frame_index,
            "url": frame.url,
            "elements": len(frame_elements),
        })

    visible = sum(1 for e in all_elements if e.get("visible"))
    sensitive = sum(1 for e in all_elements if e.get("sensitive_or_internal"))
    recommended = sum(1 for e in all_elements if e.get("recommended_locator"))

    tags = {}
    for e in all_elements:
        tag = e.get("tag") or "UNKNOWN"
        tags[tag] = tags.get(tag, 0) + 1

    return {
        "frames": frames_meta,
        "summary": {
            "total": len(all_elements),
            "visible": visible,
            "hidden": len(all_elements) - visible,
            "sensitive_or_internal": sensitive,
            "with_recommended_locator": recommended,
            "tags": tags,
        },
        "elements": all_elements,
    }


def map_current_screen(context, sequence, screen_name):
    page = wait_for_page_ready(context)

    if page is None:
        raise RuntimeError("Nenhuma página ativa encontrada.")

    count = page_relevant_count(page)

    if count <= 0:
        raise RuntimeError(
            "A página ativa foi encontrada, mas ainda possui 0 elementos mapeáveis. "
            "Aguarde a tela carregar e tente novamente."
        )

    try:
        title = page.title()
    except Exception:
        title = ""

    try:
        url = page.url
    except Exception:
        url = ""

    collected = collect_page(page)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = slugify(screen_name or title or f"pagina-{sequence:02d}")

    data = {
        "mapper_version": "2.0",
        "generated_at": datetime.now().isoformat(),
        "sequence": sequence,
        "screen_name": screen_name,
        "page": {"title": title, "url": url},
        **collected,
    }

    json_path = OUTPUT_DIR / f"{sequence:02d}_{slug}_{timestamp}.json"
    json_text = json.dumps(data, ensure_ascii=False, indent=2)
    json_path.write_text(json_text, encoding="utf-8")
    (OUTPUT_DIR / "ultimo_mapeamento.json").write_text(json_text, encoding="utf-8")

    print("")
    print("=" * 76)
    print(f"MAPEAMENTO {sequence:02d} CONCLUÍDO")
    print("=" * 76)
    print(f"Tela: {screen_name or title or '[sem título]'}")
    print(f"URL: {url}")
    print(f"Total de elementos: {data['summary']['total']}")
    print(f"Elementos visíveis: {data['summary']['visible']}")
    print(f"Locators únicos recomendados: {data['summary']['with_recommended_locator']}")
    print(f"Elementos internos/sensíveis protegidos: {data['summary']['sensitive_or_internal']}")
    print(f"Frames: {len(data['frames'])}")
    print(f"Arquivo: {json_path}")
    print("=" * 76)
    print("")

    return str(json_path)


def show_open_pages(context):
    alive = [page for page in context.pages if not page.is_closed()]

    if not alive:
        print("Nenhuma página/aba ativa.")
        return

    print("")
    print("Páginas/abas detectadas:")

    for index, page in enumerate(alive):
        try:
            title = page.title()
        except Exception:
            title = ""

        try:
            url = page.url
        except Exception:
            url = ""

        print(
            f"  [{index}] score={page_score(page)} "
            f"elementos={page_relevant_count(page)} "
            f"title={title!r} url={url}"
        )

    selected = get_active_page(context)
    if selected is not None:
        try:
            selected_url = selected.url
        except Exception:
            selected_url = ""
        print(f"Página escolhida automaticamente: {selected_url}")

    print("")


def main():
    print("")
    print("=" * 76)
    print("HOT - MAPEADOR MULTITELAS / AUDITOR DE LOCATORS v2.0")
    print("=" * 76)
    print("Melhorias:")
    print("  - espera a página carregar antes de mapear;")
    print("  - escolhe automaticamente a melhor aba/página HOT;")
    print("  - calcula matches e unique de cada locator;")
    print("  - gera recommended_locator apenas quando seguro;")
    print("  - detecta labels associados aos campos;")
    print("  - não grava passwords, CSRF, reCAPTCHA ou tokens;")
    print("  - mantém suporte a múltiplos frames.")
    print("=" * 76)
    print("")

    session_files = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1600, "height": 900})
        page = context.new_page()

        print(f"Abrindo HOT: {HOT_URL}")
        page.goto(HOT_URL, wait_until="domcontentloaded")

        print("")
        print("Faça login e navegue normalmente.")
        print("Quando quiser registrar uma etapa, volte ao terminal.")
        print("")

        sequence = 1

        while True:
            command = input(
                "[ENTER] mapear tela atual | [P] listar páginas | [Q] finalizar: "
            ).strip().lower()

            if command == "q":
                break

            if command == "p":
                show_open_pages(context)
                continue

            page = wait_for_page_ready(context)

            if page is None:
                print("\n[ERRO] Nenhuma página ativa foi encontrada.\n")
                continue

            try:
                current_title = page.title()
            except Exception:
                current_title = ""

            try:
                current_url = page.url
            except Exception:
                current_url = ""

            print("")
            print(f"Título atual: {current_title}")
            print(f"URL atual: {current_url}")
            print(f"Elementos detectados antes do mapeamento: {page_relevant_count(page)}")
            print("")

            screen_name = input(
                f"Nome da tela {sequence:02d} "
                "(ex.: login, home-hot, cadastro-estoque): "
            ).strip()

            if not screen_name:
                screen_name = f"pagina-{sequence:02d}"

            try:
                path = map_current_screen(context, sequence, screen_name)
                session_files.append(path)
                sequence += 1
            except Exception as exc:
                print("")
                print(f"[ERRO] Não foi possível mapear esta tela: {exc}")
                print("A tela NÃO foi salva. Aguarde/carregue a página e tente novamente.")
                print("")
                continue

            print("Continue no navegador para a próxima etapa.")
            print("Quando a nova tela estiver pronta, volte ao terminal.\n")

        session = {
            "mapper_version": "2.0",
            "generated_at": datetime.now().isoformat(),
            "total_mappings": len(session_files),
            "files": session_files,
        }

        session_path = OUTPUT_DIR / f"sessao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        session_path.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")

        print("")
        print("=" * 76)
        print("SESSÃO FINALIZADA")
        print("=" * 76)
        print(f"Telas mapeadas: {len(session_files)}")
        print(f"Índice da sessão: {session_path}")
        print("=" * 76)

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
