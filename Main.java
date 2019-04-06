import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		long opt_start = System.currentTimeMillis();
		int opt_iter;
		int opt_i;
		
		int page = 10;
		
		opt_iter = page / 10 -1;
		opt_i = page % 10;
		if(opt_i > 0)
			opt_iter++;
		do {
			switch(opt_i) {
			case 0:
				print();
			case 9:
				print();
			case 8:
				print();
			case 7:
				print();
			case 6:
				print();
			case 5:
				print();
			case 4:
				print();
			case 3:
				print();
			case 2:
				print();
			case 1:
				print();
			}
			
			opt_i = 0;
			opt_iter--;
		}while(opt_iter >= 0);
		
		System.out.println(System.currentTimeMillis() - opt_start);
	}

	public static void print() {
		int type = 0;
		int page = 1;

		try {
			String url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + type + "&page=" + page;

			URL obj = new URL(url);
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();
			con.setRequestProperty("Cookie", "field_list=12|0000801A;");

			BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String str;
			StringBuffer html = new StringBuffer();

			while ((str = br.readLine()) != null) {
				// System.out.println(inputLine + "\n");
				html.append(str);
			}
			br.close();

			//System.out.println("URL Content... \n" + html.toString());

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
