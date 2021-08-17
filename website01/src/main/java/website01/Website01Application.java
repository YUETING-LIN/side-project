package website01;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.mybatis.spring.annotation.MapperScan;
@SpringBootApplication
@MapperScan("website01.mapper")
public class Website01Application {

    public static void main(String[] args) {
        SpringApplication.run(Website01Application.class, args);
    }

}
