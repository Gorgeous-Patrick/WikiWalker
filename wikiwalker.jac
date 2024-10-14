import:py from wikiwalker {pre}

node Page {
  has title: str;
}

edge HyperLink {

}

walker WikiWalker {
  can calculate with Page entry {
    print("calculating", here.title);
    visit [-:HyperLink:->][0];
  }
}

with entry {
  query = "University_of_Michigan";
  # prep=pre();
  # metadata = prep[0];
  # pagerank = prep[1];
  (metadata, pagerank) = pre();
  head = Page(title=query);
  root ++> head;
  frontier = [head];
  while (len(frontier) > 0 and len(frontier) < 100) {
    cur = frontier.pop(0);
    for next_title in metadata.link_data[cur.title] {
      next_node = Page(title=next_title);
      cur +:HyperLink:+> next_node;
      frontier.append(next_node);
    }
  }
  wlk_obj = head spawn WikiWalker();
}