require('dotenv').config();

const hdWalletConfig = {
  mnemonic: process.env.MNEMONIC,
  providerOrUrl: process.env.HTTP_PROVIDER,
};

module.exports = {

  networks: {
    development: {
      host: process.env.TRUFFLE_HOST,
      port: process.env.TRUFFLE_PORT,
      network_id: process.env.TRUFFLE_NETWORK_ID,
    },
  },

  compilers: {
    solc: {
      version: process.env.SOLC_VERSION,
    },
  },
};
