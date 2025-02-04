node  Page {
  text: string = "Wikipedia Page Text for Jac";
  title: string = "Jac";
}

edge  HyperLink {
  rank: float;
  title: str;
}

walker  WikiWalker on Page { # <-- Running on DPU, All data in Page is loaded on to DPU
  has accumulated: torch.tensor;
  has const lstm: LSTM();
  can calculate with Page entry {
    # 1. Load the text from page
    text = here.text;
    # 2. Accumulate the LSTM
    embedding =  lstm.calculate(text); # <-- Calculates the LSTM embedding of the text
    self.accumulated += embedding;
    # 3. Get the hyperlinks
    possible = [-:HyperLink:->];
    next = next_page(possible);
    # 4. If there is a next page, visit it.
    if next is not None {
      visit next;
    }
  }
}


with entry { # <-- Running on CPU
  # 0. Initialize the titles
  titles = [...]; # <-- List of titles in the network
  # 1. Construct the network.
  pages, edges = fetch_html_and_construct_network(titles); 
  # 2. Initialize the scheduler
  scheduler = Scheduler(pages, edges, dpus);
  dpus = allocate_dpus(scheduler = scheduler);
  while (true) {
    # 3. Initialize the walker
    walker = WikiWalker();
    walker.accumulated = lstm;
    walker.seq = [];

    # 4. Start the walk.
    request = get_request();
    dpus.run(walker, request);
  }
}