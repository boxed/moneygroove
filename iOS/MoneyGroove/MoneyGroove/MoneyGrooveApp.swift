import SwiftUI

class Groove: Identifiable, Decodable {
    var benchmark_by_date: [Int: Int]
}

class Store: ObservableObject {
    @Published var amount: Int?
    @Published var amountTomorrow: Int?
    
    func refresh(username: String, password: String) {
        let url = URL(string: "https://moneygroove.kodare.com/api/v1/groove/")!
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        request.setValue(username, forHTTPHeaderField: "x-username")
        request.setValue(password, forHTTPHeaderField: "x-password")

        let dataTask = URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let error = error {
                print("Request error: ", error)
                return
            }

            guard let response = response as? HTTPURLResponse else { return }

            if response.statusCode == 200 {
                guard let data = data else { return }
                DispatchQueue.main.async {
                    do {
                        let foo = try JSONDecoder().decode(Groove.self, from: data)
                        self.amount = foo.benchmark_by_date[Calendar.current.component(.day, from: Date())]
                        let tomorrow = Calendar.current.date(byAdding: DateComponents(day: 1), to: Date())!
                        self.amountTomorrow = foo.benchmark_by_date[Calendar.current.component(.day, from: tomorrow)]
                    } catch let error {
                        print("Error decoding: ", error)
                    }
                }
            }
        }

        dataTask.resume()
    }
}


@main
struct MoneyGrooveApp: App {
    var store = Store()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .preferredColorScheme(.dark)
                .environmentObject(store)
        }
    }
}
