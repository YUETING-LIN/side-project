package website01.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import website01.Model.MemberInformation;
import website01.mapper.SignupMapper;

@Service
@Transactional
public class UserServiceImpl implements UserService {
    @Autowired
    private SignupMapper signupMapper;

    @Override
    public void register(MemberInformation memberInformation) {
        //密碼加密
        BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
        String password = passwordEncoder.encode(memberInformation.getPassword());
        memberInformation.setPassword(password);
        signupMapper.insertMember(memberInformation);
    }
    @Override
    public void register2(MemberInformation memberInformation) {
        //權限表的寫入
        MemberInformation memberInformation1=signupMapper.findbyUsername(memberInformation);
        signupMapper.insertAuthority(memberInformation1);
    }
   /* @Override
    public memberInformation login(String username, String password) {
        return memberRepository.login(username, password);
    }*/
}

