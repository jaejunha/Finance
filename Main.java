
public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		long opt_start = System.currentTimeMillis();
		int opt_iter;
		int opt_i;

		int test_n = 1000000008;

		int s = 0;
		opt_iter = test_n / 10 - 1;
		opt_i = test_n % 10;
		if ((test_n % 10) > 0)
			opt_iter++;
		
		do {
			switch(opt_i) {
			case 0:
				s++;
			case 9:
				s++;
			case 8:
				s++;
			case 7:
				s++;
			case 6:
				s++;
			case 5:
				s++;
			case 4:
				s++;
			case 3:
				s++;
			case 2:
				s++;
			case 1:
				s++;	
			}
			
			opt_i = 0;
		} while (opt_iter-- > 0);
		System.out.println(s);

		System.out.println(System.currentTimeMillis() - opt_start);	
	}

}
