package website01.service;

import org.apache.ibatis.annotations.Mapper;
import website01.Model.MemberInformation;
@Mapper
public interface UserService {
    void register(MemberInformation memberInformation);
    void register2(MemberInformation memberInformation);
    //MemberInformation login(String username, String password);
}
