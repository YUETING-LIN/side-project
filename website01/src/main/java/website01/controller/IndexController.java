package website01.controller;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class IndexController {

     @GetMapping("/toRestaurant")
     public String toRestaurant(){
       return "client/restaurant";
   }
     @GetMapping("/")
     public String toHomepage(){
        return "index";
    }
     @GetMapping("/toSignup")
     public String toSignup(){
        return "client/signup";
    }
     @GetMapping("/userLogin")
     public String login(){
        return "client/login";
    }


}
