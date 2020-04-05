//
//  ViewController.swift
//  simpleTimer
//
//  Created by rohan on 12/1/19.
//  Copyright © 2019 rohan. All rights reserved.
//

import Cocoa

class ViewController: NSViewController {

    @IBOutlet weak var nameField: NSTextField!
    
    @IBOutlet weak var helloText: NSTextField!
    
    @IBAction func helloButton(_ sender: Any) {
        var name = nameField.stringValue
        if name.isEmpty {
            name = "World"
        }
        helloText.stringValue = "Hello \(name)"
    }
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override var representedObject: Any? {
        didSet {
        // Update the view, if already loaded.
        }
    }


}

