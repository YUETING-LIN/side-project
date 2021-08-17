package website01.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import website01.Model.MemberInformation;

import javax.imageio.ImageIO;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import website01.service.UserService;
import website01.utils.ValidateImageCodeUtils;

import java.awt.image.BufferedImage;
import java.io.IOException;

@Controller
@RequestMapping("/user")
public class UserController {
    @Autowired
    private UserService userService;

    // 注册方法
    @PostMapping("/register")
    public String register(MemberInformation memberInformation, String code, HttpSession session) {
        String sessionCode = (String)session.getAttribute("code"); // 生成的验证码
        // 忽略大小写, 比较用户输入的验证码与生成的验证码
        if (sessionCode.equalsIgnoreCase(code)) { // 输入正确
            userService.register(memberInformation); // 注册
            userService.register2(memberInformation);
            return "redirect:/"; // 注册成功跳转到登录界面
        } else { // 输入错误
            return "redirect:/toSignup"; // 注册失败跳转到注册界面
        }
    }
    @GetMapping("/code")
    public void getImage(HttpSession session, HttpServletResponse response) throws IOException {
        // 生成验证码
        String securityCode = ValidateImageCodeUtils.getSecurityCode();
        BufferedImage image = ValidateImageCodeUtils.createImage(securityCode);
        // 存入session作用域中
        session.setAttribute("code", securityCode);
        // 响应图片
        ServletOutputStream os = response.getOutputStream();
        ImageIO.write(image, "png", os);
    }


}
