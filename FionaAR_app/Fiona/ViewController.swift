//
//  ViewController.swift
//  Fiona
//
//  Created by Timur Ryspekov on 03.10.2021.
//

import UIKit
import ARKit
import SceneKit.ModelIO

import SceneKit

class EarthNode: SCNNode {
    override init() {
        super.init()
        self.geometry = SCNSphere(radius: 0.2)
        self.geometry?.firstMaterial?.diffuse.contents = UIImage(named:"Diffuse")
        self.geometry?.firstMaterial?.specular.contents = UIImage(named:"Specular")
        self.geometry?.firstMaterial?.emission.contents = UIImage(named:"Emission")
        self.geometry?.firstMaterial?.normal.contents = UIImage(named:"Normal")
        self.geometry?.firstMaterial?.isDoubleSided = true

        self.geometry?.firstMaterial?.transparency = 1
        self.geometry?.firstMaterial?.shininess = 50
        
        let action = SCNAction.rotate(by: 360 * CGFloat((Double.pi)/180), around: SCNVector3(x:0, y:1, z:0), duration: 8)
        
        let repeatAction = SCNAction.repeatForever(action)
        
        self.runAction(repeatAction)
        
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
    }
    
    
}

class CustomButton: UIButton {

    var color: UIColor = .black
    let touchDownAlpha: CGFloat = 0.3

    func setup() {
        backgroundColor = .clear
        layer.backgroundColor = color.cgColor

        layer.cornerRadius = 12
        clipsToBounds = true
    }
    override func awakeFromNib() {
        super.awakeFromNib()

        if let backgroundColor = backgroundColor {
            color = backgroundColor
        }

        setup()
    }
}

extension String
{
    func replace_char(target: String, withString: String) -> String
    {
        return self.replacingOccurrences(of: target, with: withString, options: NSString.CompareOptions.literal, range: nil)
    }
    
    func encodeUrl() -> String?
    {
        return self.addingPercentEncoding( withAllowedCharacters: .urlQueryAllowed)
    }
    func decodeUrl() -> String?
    {
        return self.removingPercentEncoding
    }
    
}


extension String {

    var parseJSONString: AnyObject? {

        let data = self.data(using: String.Encoding.utf8, allowLossyConversion: false)

        if let jsonData = data {
            do{
            // Will return an object or nil if JSON decoding fails
            return try JSONSerialization.jsonObject(with: jsonData, options: JSONSerialization.ReadingOptions.mutableContainers) as AnyObject
            }
            catch{
                return nil
            }
        } else {
            // Lossless conversion of the string was not possible
            return nil
        }
    }
}

class ViewController: UIViewController {

    private let configuration = ARWorldTrackingConfiguration()
    @IBOutlet weak var sceneView: ARSCNView!
    override func viewDidLoad() {
        super.viewDidLoad()
        self.sceneView.showsStatistics = true
        
        //self.sceneView.debugOptions = [ARSCNDebugOptions.showFeaturePoints]
        
        addTapGesture()
        addEarth2()
    }
    
    
    @IBOutlet weak var url_field: UITextField!
    
    var api_url = ""
    private func addTapGesture() {
            let tapGesture = UITapGestureRecognizer(target: self, action: #selector(didTap(_:)))
            self.sceneView.addGestureRecognizer(tapGesture)
        }
    
    
    override func viewWillAppear(_ animated: Bool) {
           super.viewWillAppear(animated)
           self.sceneView.session.run(configuration)
       }
    
       override func viewWillDisappear(_ animated: Bool) {
           super.viewWillDisappear(animated)
           self.sceneView.session.pause()
       }
    
    private var node: SCNNode!
     
    func addEarth(x: Float = 0, y: Float = 0, z: Float = 0.0) {
        
        
        
        
        guard let shipScene = SCNScene(named: "arassets.scnassets/earth.scn"),
            let shipNode = shipScene.rootNode.childNode(withName: "earth", recursively: false)
        else {
            return
        }
        shipNode.scale = SCNVector3(0.1, 0.1, 0.1)
        shipNode.position = SCNVector3(x,y,z)
        sceneView.scene.rootNode.addChildNode(shipNode)
    }
    
    func addEarth2(x: Float = 0, y: Float = 0, z: Float = 0.0) {
        
        
        let position = SCNVector3(x: x, y: y, z: z)
        
        let newEarth = EarthNode()
        newEarth.position = position
        
        sceneView.scene.rootNode.addChildNode(newEarth)
    }
    
    
    func addObject(x: Float, y: Float,z: Float, capRadius: Float, height: Float) {
           
        let box = SCNCapsule(capRadius: CGFloat(0.001), height: CGFloat(0.005))
     
          
            let colors = [UIColor.red, // front
                UIColor.red, // right
                UIColor.red, // back
                UIColor.red, // left
                UIColor.red, // top
                UIColor.red] // bottom
            let sideMaterials = colors.map { color -> SCNMaterial in
                let material = SCNMaterial()
                material.diffuse.contents = color
                material.locksAmbientWithDiffuse = true
                return material
            }
            box.materials = sideMaterials
     
           
            self.node = SCNNode()
            self.node.geometry = box
            self.node.position = SCNVector3(x, y, z)
     
            
            sceneView.scene.rootNode.addChildNode(self.node)
        }
    
    @objc func didTap(_ gesture: UIPanGestureRecognizer) {
        
            let tapLocation = gesture.location(in: self.sceneView)
            let results = self.sceneView.hitTest(tapLocation, types: .featurePoint)
     
            
            guard let result = results.first else {
                return
            }
        
            print(result)
        }
    
    
   
    var texts = [] as [String]
    
    
    func get_data(){
       
        let url = URL(string: api_url)
        guard let requestUrl = url else { fatalError() }

        var request = URLRequest(url: requestUrl)
        request.httpMethod = "POST"

        // Set HTTP Request Header
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let json_str = "{\"token\": \""+"your_key_here"+"\"}"
        do{
            let jsonData = try JSONSerialization.data(withJSONObject: json_str.parseJSONString as Any)

        request.httpBody = jsonData

            let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
                
                if let error = error {
                    print("Error took place \(error)")
                    return
                }
                guard let data = data else {return}
                DispatchQueue.main.async {
                do{
                   if let json = try JSONSerialization.jsonObject(with: data, options: []) as? NSDictionary {
                    
                    if let all_data = json["data"] as? NSArray{
                        var i = 0
                       
                        self.texts.removeAll()
                        
                        while i < all_data.count{
                            if let data_object = all_data[i] as? NSArray{
                                print(data_object)
                                var x = 0.0 as Float
                                if let x1 = data_object[0]  as? NSNumber{
                                    x = x1.floatValue
                                }
                                
                                var y = 0.0 as Float
                                if let y1 = data_object[1]  as? NSNumber{
                                    y = y1.floatValue
                                }
                                
                                var z = 0.0 as Float
                                if let z1 = data_object[2]  as? NSNumber{
                                    z = z1.floatValue
                                }
                                
                                var cr = 0.0001 as Float
                                if let cr1 = data_object[2]  as? NSNumber{
                                    cr = cr1.floatValue
                                }
                                
                                var h = 0.0005 as Float
                                if let h1 = data_object[2]  as? NSNumber{
                                    h = h1.floatValue
                                }
                                
                                
                                print(x,y,z)
                                self.addObject(x: x , y: y , z: z  ,capRadius: cr, height: h);
                                
                                
                            }
                            i+=1;
                        }
                        
                       
                    }
                    
                    
                    }
                  
                }catch let jsonErr{
                    print(jsonErr)
                    
                }
               
                }
                   
                
                    
              
                
               
                
         
        }
        task.resume()
        
        
        }
        catch{
        
            
        }
        
    }
    
    func wrong_data(){
        let message = "Wrong E-mail or password"
         let alert = UIAlertController(title: "Error", message: message, preferredStyle: UIAlertController.Style.alert)
                
        
                
          alert.addAction(UIAlertAction(title: "Ok", style: .default, handler: nil))
         self.present(alert, animated: true, completion: nil)
    }

    @IBAction func show_btn_click(_ sender: Any) {
        api_url = url_field.text ?? "your_api_here"
        print(api_url)
        get_data()
    }
}

