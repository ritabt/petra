#include <stdio.h>

struct my_struct
{
	int a, b, c;
};

//given a struct with elements all one digit ints, return the ints right next to each other (3 digit int)
int test_struct_input(struct my_struct x){
	return x.a * 100 + x.b * 10 + x.c;
}

//given 3 ints put them in the struct my_struct and return that
struct my_struct test_struct_output(int a, int b, int c){
	struct my_struct output;
	output.a = a;
	output.b = b;
	output.c = c;
	return output;
}

int main(){
	struct my_struct x = {4, 4, 4};
	printf("%d\n", test_struct_input(x));
	printf("%d\n", test_struct_input(test_struct_output(5, 5, 5)));
}
