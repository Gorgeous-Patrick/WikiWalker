import:py json;
import:py from utils {network_path, Network, pagerank_path, PageInfo, run_path}
import:py from datetime {datetime}
# from utils import network_path, Network, pagerank_path, PageInfo
# from datetime import datetime
# from utils import run_path


can pre() {

    with open(network_path, "r") as network_file, open(
        pagerank_path, "r"
    ) as pagerank_file {
        parsed_network = json.load(network_file);
        network = Network(**parsed_network);
        parsed_pagerank = json.load(pagerank_file);
        return (network, parsed_pagerank);
    }
}


can read_page_text(title: str) {
    with open(f"data/cache/{title.replace('/', '_')}.json", "r") as file {

        parsed = json.load(file);
        page = PageInfo(**parsed);
        return page.text;
    }
}


can post(result: list[str]) {

    if not run_path.exists() {

        run_path.mkdir();
    }
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f");
    with open(run_path / f"{timestamp}.json", "w") as file {
        file.write(json.dumps(result));
    }
}
