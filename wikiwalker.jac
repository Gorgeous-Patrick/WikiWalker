import:py from wikiwalker {pre}

node Page {
  has title: str;
}

edge HyperLink {

}

walker WikiWalker {
  can calculate with Page entry {
    print("calculating", here.title);
    if len([-:HyperLink:->]) > 0{

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
  wlk_obj = head spawn WikiWalker();
}