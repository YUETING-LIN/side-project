package website01.config;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.security.config.annotation.authentication.builders.*;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.*;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.authentication.rememberme.JdbcTokenRepositoryImpl;

import javax.sql.DataSource;

@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private DataSource dataSource;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {

        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        String userSQL = "select username,password,valid from memberdata where username =?";
        String authoritySQL = "SELECT c.username,a.authority FROM memberdata c ,t_authority a ,t_customer_authority ca WHERE ca.customer_id=c.id AND ca.authority_id=a.id and c.username=?";
        auth.jdbcAuthentication().passwordEncoder(encoder).dataSource(dataSource).usersByUsernameQuery(userSQL).authoritiesByUsernameQuery(authoritySQL);

    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        //http.csrf().disable(); 關閉csrf功能
        http.authorizeRequests().antMatchers("/").permitAll().antMatchers("/**").permitAll().anyRequest().authenticated();
               // .antMatchers("/detail/common/**").hasRole("common")
               // .antMatchers("/detail/vip/**").hasRole("vip")
        http.formLogin().loginPage("/userLogin").permitAll()
                .usernameParameter("username").defaultSuccessUrl("/").failureUrl("/userLogin?error");
        http.logout().logoutUrl("/mylogout").logoutSuccessUrl("/");
        //http.rememberMe().rememberMeParameter("rememberme").tokenValiditySeconds(200).tokenRepository(tokenRepository());

    }
}
