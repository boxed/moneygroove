import SwiftUI

let defaults = UserDefaults.init(suiteName: "group.moneygroove")

struct ContentView: View {
    @AppStorage("username", store: defaults) var username: String = ""
    @AppStorage("password", store: defaults) var password: String = ""
    
    @EnvironmentObject var store: Store
    
    var body: some View {
        VStack {
            Text("Money groove")
            Form {
                TextField(text: $username, prompt: Text("Username")) {
                    Text("Username")
                }
                SecureField(text: $password, prompt: Text("Password")) {
                    Text("Password")
                }
            }
            if let amount = store.amount {
                Text("\(amount)").font(.system(size: 80))
            }
            if let amount = store.amountTomorrow {
                Text("\(amount)").font(.system(size: 50))
            }
            Spacer(minLength: 400)
        }
        .onAppear {
            store.refresh(username: username, password: password)
        }
    }
}

#Preview {
    ContentView().environmentObject(Store())
}
