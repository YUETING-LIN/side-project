package website01.mapper;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import website01.Model.MemberInformation;
import website01.Model.RestaurantSearch;

import java.util.List;

public interface RestaurantMapper {
    @Select("SELECT restName,branchName,county,area,elseAddress,tel FROM restaurantall11 WHERE county=#{county} and area=#{area}AND week=#{week}and time LIKE '%${time}%'")
    public List<RestaurantSearch> selectRestaurantResult(RestaurantSearch restaurantSearch);//訪客 餐廳基礎搜尋
    @Insert("INSERT INTO t_customer_authority(`customer_id`, `authority_id`) VALUES (#{id},#{valid})")
    public void insertAuthority(RestaurantSearch restaurantSearch);
}
