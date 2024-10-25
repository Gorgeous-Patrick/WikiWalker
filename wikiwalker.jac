import:py from wikiwalker {pre}
import:py from fetch {fetch_text}
import:py from lstm {initial}
import:py from lstm {calculate}
import:py json;
import:py from random {choice, seed}
import:py from os {environ}

node Page {
  has title: str;
  has pagerank: float;
}

edge HyperLink {

}

walker WikiWalker {
  has accumulated: torch.tensor;
  has seq: list[str];
  can calculate with Page entry {
    self.seq.append(here.title);
    text = fetch_text(here.title);
    self.accumulated = calculate(self.accumulated, text, 0.5);
    possible = [-:HyperLink:->] + [<-:HyperLink:-];
    possible = [next_page for next_page in possible if next_page.title not in self.seq];
    max_page = None;
    max_rank = 0;
    for page in possible {
      if page.pagerank > max_rank {
        max_rank = page.pagerank;
        max_page = page;
      }
    }
    if max_page is not None {
      visit max_page;
    }
  }
}

with entry {
  # prep=pre();
  # metadata = prep[0];
  # pagerank = prep[1];
  rand_seed = environ.get("SEED",0);
  print("Random Seed", rand_seed);
  seed(rand_seed);
  (metadata, pagerank) = pre();
  rootName = "Conflict-driven_clause_learning";
  head = Page(title=rootName, pagerank=pagerank[rootName]);
  root ++> head;
  frontier = [head];
  content_list = {head.title: head};
  while (len(frontier) > 0 and len(frontier) < 100) {
    cur = frontier.pop(0);
    # maxrank = 0.0;
    # maxnode = None;
    for next_title in metadata.link_data[cur.title] {
      if (next_title not in metadata.link_data.keys()) {
        continue;
      }
      next_node = Page(title=next_title, pagerank=pagerank[next_title]);
      frontier.append(next_node);
      cur +:HyperLink:+> next_node;
      content_list[next_node.title] = next_node;

    }
  }
  query = choice(list(content_list.keys()));
  print(content_list.keys());
  wlk_obj = content_list[query] spawn WikiWalker(accumulated=initial(), seq=[]);
  print(wlk_obj.accumulated);
  print(wlk_obj.seq);
  file = open("single_result.json", "w");
  json.dump(wlk_obj.seq, file);
  file.close();
}