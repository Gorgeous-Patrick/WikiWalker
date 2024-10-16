import:py from wikiwalker {pre}
import:py from fetch {fetch_text}
import:py from lstm {initial}
import:py from lstm {calculate}

node Page {
  has title: str;
}

edge HyperLink {

}

walker WikiWalker {
  has accumulated: torch.tensor;
  can calculate with Page entry {
    print("calculating", here.title);
    if len([-:HyperLink:->]) > 0{
      text = fetch_text(here.title);
      self.accumulated = calculate(self.accumulated, text, 0.5);
      visit [-:HyperLink:->][0];
    }
  }
}

with entry {
  query = "Conflict-driven_clause_learning";
  # prep=pre();
  # metadata = prep[0];
  # pagerank = prep[1];
  (metadata, pagerank) = pre();
  head = Page(title=query);
  root ++> head;
  frontier = [head];
  while (len(frontier) > 0 and len(frontier) < 100) {
    cur = frontier.pop(0);
    maxrank = 0.0;
    maxnode = None;
    for next_title in metadata.link_data[cur.title] {
      next_node = Page(title=next_title);
      if (maxrank < pagerank[next_title]) {
        maxnode = next_node;
        maxrank = pagerank[next_title];
      }
      frontier.append(next_node);
    }
    if maxnode is not None {
      cur +:HyperLink:+> maxnode;
    }
  }
  wlk_obj = head spawn WikiWalker(accumulated=initial());
  print(wlk_obj.accumulated);
}