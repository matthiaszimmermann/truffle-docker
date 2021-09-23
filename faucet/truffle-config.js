require('dotenv').config();

const HDWalletProvider = require('@truffle/hdwallet-provider');
const { settings } = require('./package');

const hdWalletConfig = {
  mnemonic: process.env.MNEMONIC,
  providerOrUrl: process.env.HTTP_PROVIDER,
};

module.exports = {

  networks: {
    development: {
      provider: () => new HDWalletProvider(hdWalletConfig),
      host: process.env.TRUFFLE_HOST,
      port: process.env.TRUFFLE_PORT,
      network_id: process.env.TRUFFLE_NETWORK_ID,
    },
  },

  // mocha: {
  //   timeout: 30000,
  //   useColors: true,
  // },

  compilers: {
    solc: {
      version: "0.8.0",
  //     settings: {
  //       optimizer: {
  //         enabled: true,
  //         runs: 200,
  //       },
  //       evmVersion: 'byzantium', 
  //       evmTarget: 'byzantium', 
  //     },
    },
  },
};
