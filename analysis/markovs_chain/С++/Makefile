all:
	g++ -std=c++11 -lstdc++  main.cpp Graph.cpp -o graph
asan:
	g++ -fsanitize=address,leak,undefined main.cpp Graph.cpp -o graph
run:
	./graph.out
