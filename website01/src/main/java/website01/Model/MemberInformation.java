package website01.Model;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class MemberInformation {
        private String id;
        private String username;
        private String email;
        private String name;
        private String password;
        private String birthday;
        private String valid;
}