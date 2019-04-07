
public class Item {
	private String code;
	private int price;
	private String changed;
	private String PER, ROE, PBR;
	
	private int max, min;

	public Item(String code, int price, String changed, String PER, String ROE, String PBR) {
		this.code = code;
		this.price = price;
		this.changed = changed;
		this.PER = PER;
		this.ROE = ROE;
		this.PBR = PBR;
	}

	public String getCode() {
		return code;
	}

	public void setCode(String code) {
		this.code = code;
	}

	public int getPrice() {
		return price;
	}

	public void setPrice(int price) {
		this.price = price;
	}
	
	public String getChanged() {
		return changed;
	}

	public void setChanged(String changed) {
		this.changed = changed;
	}

	public String getPER() {
		return PER;
	}

	public void setPER(String pER) {
		PER = pER;
	}

	public String getROE() {
		return ROE;
	}

	public void setROE(String rOE) {
		ROE = rOE;
	}

	public String getPBR() {
		return PBR;
	}

	public void setPBR(String pBR) {
		PBR = pBR;
	}
	
	public int getMin() {
		return min;
	}
	
	public void setMin(int min) {
		this.min = min;
	}
	
	public int getMax() {
		return max;
	}
	
	public void setMax(int max) {
		this.max = max;
	}
}
