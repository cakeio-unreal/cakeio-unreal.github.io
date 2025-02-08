# Advanced Cake IO
Welcome to the advanced section of CakeIO! All of the sections in this area will assume that users are comfortable and familiar with fundamental principles established in the [Core API](/core-api) section.

## Tour of Advanced Features
This section will give a brief tour of the advanced sections covered in this documentation. 

## Utility Libraries 
There are two higher level library implementations that are built on CakeIO's core objects: CakeMix and CakeAsyncIO. These libraries will continue to expand and be refined as the CakeIO API matures.

### CakeMix 
{{ link_cakemix() }} is a utility library that offers a variety of high level operations on CakeDir, CakeFile, and CakePath objects. There are two implementations, one for C++ and one for Blueprint. This library is meant to serve as a starting point for users who are seeking a prebuilt solution to some common, complex IO operations. It also serves as an experimental grounds where CakeIO can test out designs and interfaces that might some day be promoted to the CoreAPI. 

### CakeAsyncIO 
{{ link_cakeasyncio() }} is a library that offers asynchronous interfaces to Core and CakeMix IO operations. There are two implementations, one for C++ and one for Blueprint. There are numerous more limitations on async operations in Blueprint, and so the coverage between the two implementations varies. Regardless, these are meant to be serve as a helpful resource for users to be able to accomplish asynchronous IO in a relatively simple manner. 

## CakeIO Services
The {{ link_cakeservices() }} are the lowest level of CakeIO. They are the interfaces that wrap the underlying Unreal IO operations, and they are what the Core CakeIO API is built upon. C++ users of CakeIO can also take advantage of this API when they desire to build their own IO solutions if the Core API is insufficient for their needs. Be warned, though, the service APIs are much lower level and error-prone than using the Core API!

