package website01.Model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class RestaurantSearch {
    private String restName;
    private String branchName;
    private String county;
    private String area;
    private String elseAddress;
    private String week;
    private String time;
    private Integer minp;
    private Integer maxp;
    private String tel ;

    public String addressString() {
        return county+area+elseAddress;
    }
}
