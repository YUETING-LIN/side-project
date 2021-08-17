package website01.mapper;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import website01.Model.MemberInformation;


public interface SignupMapper {
     @Insert("INSERT INTO memberdata(`username`, `name`, `password`, `email`, `birthday`) VALUES (#{username}, #{name},#{password},#{email},#{birthday})")
     public void insertMember(MemberInformation memberInformation);//建立會員資料
     @Select("select ID,valid from memberdata where username =#{username}")
     public MemberInformation findbyUsername(MemberInformation memberInformation);//搜尋會員
     @Insert("INSERT INTO t_customer_authority(`customer_id`, `authority_id`) VALUES (#{id},#{valid})")
     public void insertAuthority(MemberInformation memberInformation);//會員權限建立
}
