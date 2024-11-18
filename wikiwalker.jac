import:jac from wikiwalkerlib {pre, read_page_text, post}
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
    text = read_page_text(here.title);
    # self.accumulated = calculate(self.accumulated, text, 0.5);
    possible = [-:HyperLink:->];
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
  (network, pagerank) = pre();
  content_list = {};
  # Reconstruct the network
  for title in network.nodes {
    content_list[title] = Page(title=title, pagerank=pagerank[title]);
  }
  for title in network.nodes {
    for next_title in network.links[title] {
      content_list[title] +:HyperLink:+> content_list[next_title];
    }
  }
  # while (len(frontier) > 0 and len(frontier) < 100) {
  #   cur = frontier.pop(0);
  #   # maxrank = 0.0;
  #   # maxnode = None;
  #   for next_title in network.links[cur.title] {
  #     if (next_title not in metadata.link_data.keys()) {
  #       continue;
  #     }
  #     next_node = Page(title=next_title, pagerank=pagerank[next_title]);
  #     frontier.append(next_node);
  #     cur +:HyperLink:+> next_node;
  #     content_list[next_node.title] = next_node;

  #   }
  # }
  while True {
    query = choice(list(content_list.keys()));
    wlk_obj = content_list[query] spawn WikiWalker(accumulated=initial(), seq=[]);
    print(wlk_obj.accumulated);
    print(wlk_obj.seq);
    post(wlk_obj.seq);
  }
}