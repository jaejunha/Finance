import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;

public class Main {

	private static int int_currentPage = 1;
	private static int int_currentType = 1;
	private static HashMap<String, Item> map_raw, map_candidate;
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

		long opt_start = System.currentTimeMillis();
		int opt_iter;
		int opt_i;
		
		int int_page = 10;
		double double_basePBR = 1.0;
		double double_basePER = 15;
		double double_basePercent = 20.0;
		
		map_raw = new HashMap<>();
		map_candidate = new HashMap<>();
		
		opt_iter = int_page / 10 -1;
		opt_i = int_page % 10;
		if(opt_i > 0)
			opt_iter++;
		do {
			switch(opt_i) {
			case 0:
				collectItem();
				int_currentPage++;
			case 9:
				collectItem();
				int_currentPage++;
			case 8:
				collectItem();
				int_currentPage++;
			case 7:
				collectItem();
				int_currentPage++;
			case 6:
				collectItem();
				int_currentPage++;
			case 5:
				collectItem();
				int_currentPage++;
			case 4:
				collectItem();
				int_currentPage++;
			case 3:
				collectItem();
				int_currentPage++;
			case 2:
				collectItem();
				int_currentPage++;
			case 1:
				collectItem();
				int_currentPage++;
			}
			
			opt_i = 0;
			opt_iter--;
		}while(opt_iter >= 0);

		Iterator<String> iter;
		String key;
		Item item;
		
		iter = map_raw.keySet().iterator();
		while (iter.hasNext()) {
		    key = iter.next();
		    item = map_raw.get(key);
		    
		    /* skip minus */
		    if(item.getPER().contains("-") || item.getROE().contains("-") || item.getPBR().contains("-"))
		    	continue;
		    
		    /* check base PER */
		    if(item.getPER().contains("N/A") == false && Double.parseDouble(item.getPER()) > double_basePER)
		    	continue;
		    
		    /* check base PBR */
		    if(item.getPBR().contains("N/A") == false && Double.parseDouble(item.getPBR()) > double_basePBR)
		    	continue;
		    
		    map_candidate.put(key, item);
		}

		iter = map_candidate.keySet().iterator();
		LinkedList<String> list = new LinkedList<>();
		URL obj;
		HttpURLConnection con;
		BufferedReader br;
		int int_min, int_max;
		String str, url;
		double cal;
		
		while (iter.hasNext()) {
		    key = iter.next();
		    item = map_raw.get(key);
		    
		    try {
				url = "https://finance.naver.com/item/main.nhn?code=" + item.getCode();

				obj = new URL(url);
				con = (HttpURLConnection) obj.openConnection();
				br = new BufferedReader(new InputStreamReader(con.getInputStream()));
				
				while ((str = br.readLine()).contains("</table") == false);
				while ((str = br.readLine()).contains("</table") == false);
				while ((str = br.readLine()).contains("</table") == false);
				while ((str = br.readLine()).contains("</table") == false);
				while ((str = br.readLine()).contains("</table") == false);
				while ((str = br.readLine()).contains("</table") == false);
				while ((str = br.readLine()).contains("</table") == false);
				while ((str = br.readLine()).contains("</table") == false);
				while ((str = br.readLine()).contains("</tr") == false);
				while ((str = br.readLine()).contains("</em") == false);
				/* min */
				if(str.contains("N/A")) {
					list.add(key);
					map_candidate.remove(key);
					continue;
				}
				else
					int_min = Integer.parseInt(str.split("<|>")[2].replace(",", ""));
				while ((str = br.readLine()).contains("</em") == false);
				/* max */
				int_max = Integer.parseInt(str.split("<|>")[2].replace(",", ""));

				cal = 100 * (1 - (double)(item.getPrice()-int_min) / (int_max-int_min));
				if(cal > double_basePercent) {
					list.add(key);
					continue;
				}
				
				item.setMin(int_min);
				item.setMax(int_max);
				map_candidate.put(key, item);

			} catch (NullPointerException e) {
			} catch(Exception e) {
				e.printStackTrace();
			}
		}
		iter = list.iterator();
		while (iter.hasNext())
			map_candidate.remove(iter.next());
		
		System.out.println(System.currentTimeMillis() - opt_start);
	}

	public static void collectItem() {
		try {
			String url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + int_currentType + "&page=" + int_currentPage;

			URL obj = new URL(url);
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();
			con.setRequestProperty("Cookie", "field_list=12|0000801A;");

			BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String str;
			String strs[];
			
			int int_price;
			String str_code, str_title, str_changed, str_PER, str_ROE, str_PBR;

			/* skip first table */
			while ((str = br.readLine()).contains("</table") == false);
			/* skip first tr */
			while ((str = br.readLine()).contains("</tr") == false);

			/* loop tr */
			while(true) {
				/* skip first td */
				while ((str = br.readLine()).contains("</td") == false);
				
				for(int i=0;i<5;i++) {
					while ((str = br.readLine()).contains("</td") == false);
					while ((str = br.readLine()).contains("</td") == false);
					/* title */
					if(str.contains("tltle")) {
						strs = str.split("\"|<|>|=");
						str_code = strs[6];
						str_title = strs[11];
					}
					else
						return ;
					while ((str = br.readLine()).contains("</td") == false);
					/* price */
					int_price = Integer.parseInt(str.split("<|>")[2].replace(",", ""));
					while ((str = br.readLine()).contains("</td") == false);
					while ((str = br.readLine()).contains("%") == false);
					/* changed */
					if(str.contains("0.00"))
						str_changed = "0.00%";
					else
						str_changed = str.replace("\t", "");
					while ((str = br.readLine()).contains("</td") == false);
					while ((str = br.readLine()).contains("</td") == false);
					while ((str = br.readLine()).contains("</td") == false);
					while ((str = br.readLine()).contains("</td") == false);
					/* PER */
					str_PER = str.split("<|>")[2].replace(",", "");
					while ((str = br.readLine()).contains("</td") == false);
					/* ROE */
					str_ROE = str.split("<|>")[2].replace(",", "");
					while ((str = br.readLine()).contains("</td") == false);
					/* PBR */
					str_PBR = str.split("<|>")[2].replace(",", "");
					while ((str = br.readLine()).contains("</td") == false);
					map_raw.put(str_title, new Item(str_code, int_price, str_changed, str_PER, str_ROE, str_PBR));
				}
					
				/* skip blank */
				while ((str = br.readLine()).contains("</tr") == false);
				while ((str = br.readLine()).contains("</tr") == false);
				while ((str = br.readLine()).contains("</tr") == false);
			}

		} catch (NullPointerException e) {
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
}
