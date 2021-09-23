// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

contract Faucet {

    // accept any incoming amount of wei
    receive () external payable {}

    // transfer ether to anyone asking
    function withdraw(uint withdraw_amount) public {
        // limit withdrawal amount to 1 eth (=10^18 wei)
        require(withdraw_amount <= 1000000000000000000);

        // send amount to address of withdraw request
        payable(msg.sender).transfer(withdraw_amount);
    }
}