#include <dpu>
#include <iostream>
#include <unistd.h>
#include <vector>

std::vector<std::string> queries = {"query111", "query2", "query3", "query4", "query5", "query6", "query7", "query8", "query9", "query10"};
using namespace dpu;

void send_query(DpuSet &dpu, const std::string &query) {
  std::vector<char> query_v(query.begin(), query.end());
  // Find the nearest multiple of 8
  std::cout << "Sending query: ";
  for (auto & ch: query_v) {
    std::cout << ch << " ";
  }
  size_t size = (query_v.size() + 7) & ~7;
  query_v.resize(size, 0);
  dpu.copy("query", query_v, query_v.size() * 1);
  
  std::vector<uint32_t> downloaded(1);
  downloaded[0] = 1;
  std::cout << "Sending query: " << query << std::endl;

  // dpu.copy("downloaded", downloaded, 4);
  // std::cout << "Sent query: " << query << std::endl;
}

void wait_until_ready(DpuSet &dpu) {
  std::vector<std::vector<uint64_t>> ready(1);
  ready.front().resize(1);
  while (!ready[0][0]) {
    dpu.copy(ready, "ready", 8);
    std::cout << "Ready: " << ready[0][0] << std::endl;
  }
}

uint64_t get_output(DpuSet &dpu) {
  std::vector<std::vector<uint64_t>> output(1);
  output.front().resize(1);
  dpu.copy(output, "output");
  return output[0][0];
}



int main(void) {
  try {
    auto dpu = DpuSet::allocate(1);
    auto dpu_async = dpu.async();
    dpu.load("dev");
    // Change queries[0] to vector

    dpu_async.exec();
    std::cout << "Waiting for DPU to be ready..." << std::endl;
    wait_until_ready(dpu);
    std::cout << "Sending DPU data" << std::endl;
    send_query(dpu, queries[0]); // Sets the download flag
    auto output = get_output(dpu);
    std::cout << "Output: " << output << std::endl;
    dpu.log(std::cout);
  }
  catch (const DpuError & e) {
    std::cerr << e.what() << std::endl;
  }
  return 0;
}