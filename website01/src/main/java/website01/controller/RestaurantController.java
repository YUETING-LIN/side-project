package website01.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import website01.Model.RestaurantSearch;
import website01.service.RestaurantService;

import javax.servlet.http.HttpServletRequest;
import java.util.List;
@Controller
@RequestMapping("/rest")
public class RestaurantController {
    @Autowired
    private RestaurantService restaurantService;

    @PostMapping("/common")
    public String restaurantSearch(Model model ,RestaurantSearch restaurantSearch) {

        List<RestaurantSearch> rest = restaurantService.commonSearch(restaurantSearch);//訪客 搜尋功能
        model.addAttribute("rest", rest);
        return "/client/restaurant";
    }

   /* @RequestMapping("/client/restaurant")
    public String registerForm(Model model) {
        //设置一个模板去获取填写的form内容
        //将要提交的内容封装为一个类
        model.addAttribute("RestaurantSearch",new RestaurantSearch());
        return "/client/restaurant";
    }*/


}
